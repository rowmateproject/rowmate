from fastapi import Depends, APIRouter, HTTPException

import pymongo
from uuid import UUID

# models
from models.chat import Chat, AddChat
from models.chatmessage import ChatMessage, AddChatMessage, GetChatMessages

def get_user_chats_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('')
    async def get_user_chats(user=Depends(
            authenticator.get_current_active_user)):
        sort = [('_id', pymongo.DESCENDING)]
        filter = {'_id': False}
        find = {'$or':[
            {'owner':user.id},
            {'members': { '$in': [user.id] }}
        ]}

        res = await database['chats'].find(
            find, filter).sort(sort).to_list(length=150)

        if res is not None:
            return res
        else:
            raise HTTPException(status_code=404, detail='No chats were found')

    return router

def get_chat_messages_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('/messages/get')
    async def get_chat_messages(chat: GetChatMessages, user=Depends(
            authenticator.get_current_active_user)):

        filter = {'_id': False}
        find = {'uuid': chat.uuid, '$or':[
            {'owner':user.id},
            {'members': { '$in': [user.id] }}
        ]}

        res = await database['chats'].find(
            find, filter).to_list(length=10)
        if len(res) == 0:
            raise HTTPException(status_code=404, detail='Chat not found or no access')


        sort = [('_id', pymongo.DESCENDING)]
        filter = {'_id': False}
        find = {'chat': chat.uuid}

        res = await database['messages'].find(
            find, filter).sort(sort).to_list(length=150)

        if res is not None:
            return res
        else:
            raise HTTPException(status_code=404, detail='No chats were found')

    return router


def add_chat_message_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('/message/add')
    async def add_chat_message(message: AddChatMessage, user=Depends(
            authenticator.get_current_active_user)):

        message.author = user.id

        filter = {'_id': False}
        find = {'uuid': message.chat, '$or':[
            {'owner':user.id},
            {'members': { '$in': [user.id] }}
        ]}

        res = await database['chats'].find(
            find, filter).to_list(length=10)
        if len(res) == 0:
            raise HTTPException(status_code=404, detail='Chat not found or no access')
        else:
            res = await database['messages'].insert_one(dict(message))

            if res.acknowledged:
                return {'status': 'ok'}
            else:
                raise HTTPException(status_code=404, detail='No message added')

    return router


def delete_boat_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.delete('/{uuid}')
    async def delete_boat(uuid, user=Depends(
            authenticator.get_current_superuser)):
        query = { 'uuid': UUID(uuid) }
        res = await database['boats'].delete_one(query)
        if res.deleted_count > 0:
            return True
        else:
            raise HTTPException(
                status_code=404, detail='Boat was not found')

    return router


def add_chat_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('')
    async def post_chat(chat: AddChat, user=Depends(
            authenticator.get_current_active_user)):

        chat.owner = user.id
        chat.members += [user.id]
        print(chat)
        exists = await database['chats'].find({ 'members': chat.members }).to_list(length=2)
        if len(exists) == 0:
            res = await database['chats'].insert_one(dict(chat))
        else:
            raise HTTPException(status_code=400, detail='Chat already exists')

        if res.acknowledged:
            return {'status': 'ok'}
        else:
            raise HTTPException(status_code=400, detail='No chat was created')

    return router
