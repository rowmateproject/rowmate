from fastapi import Depends, Request, APIRouter, HTTPException
from uuid import UUID

import pymongo
import re

# models
from models.user import UserList


# regex
PATTERN = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def get_manage_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.post('/users/activate/{uuid}')
    async def activate_user(uuid: str, request: Request, requser=Depends(
            authenticator.get_current_superuser)):
        user = await database['users'].find_one({'id': UUID(uuid)})

        query = {'id': user['id']}
        document = {'$set': {'is_active': True, 'is_accepted': True}}

        # accepting the user when user is activated
        res = await database['users'].update_one(query, document)

        if res is not None:
            return {'status': 'ok'}
        else:
            raise HTTPException(status_code=404, detail='User not activated')

    @router.post('/users/deactivate/{uuid}')
    async def deactivate_user(uuid: str, request: Request, requser=Depends(
            authenticator.get_current_superuser)):
        user = await database['users'].find_one({'id': UUID(uuid)})

        if user is not None:
            query = {'id': user['id']}
            document = {'$set': {'is_active': False}}

            res = await database['users'].update_one(query, document)

            if res is not None:
                return {'status': 'ok'}
            else:
                raise HTTPException(
                    status_code=400, detail='User not deactivated')
        else:
            raise HTTPException(status_code=404, detail='User not found')

    @router.post('/users/invite')
    async def invite_user(users: UserList, user=Depends(
            authenticator.get_current_superuser)):
        mails = []

        for mail in users.mails:
            if not re.search(mail, PATTERN):
                mails.append({'email': mail})

        res = await database['invited'].insert_many(mails)

        if len(res.inserted_ids) == len(mails):
            return {'detail': 'Successfully added all email addreesses'}
        else:
            return {'detail': 'Not all email addreesses have been added'}

    @router.get('/users/list')
    async def list_users(user=Depends(authenticator.get_current_superuser)):
        sort = [('_id', pymongo.DESCENDING)]
        filter = {'_id': False,
                  'id': True,
                  'name': True,
                  'email': True,
                  'is_active': True,
                  'is_accepted': True,
                  'is_superuser': True,
                  'is_confirmed': True,
                  'avatar': True}

        res = await database['users'].find(
            {}, filter).sort(sort).to_list(length=150)

        if len(res) > 0:
            return {'users': res}
        else:
            print(res)

    return router
