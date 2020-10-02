from fastapi import Request, APIRouter, HTTPException
from datetime import datetime

# models
from models.user import UserDB

# main
from app import db


async def activate_user(user: UserDB):
    if user['is_accepted'] and user['is_confirmed']:
        query = {'id': user['id']}
        filter = {'$set': {'is_active': True}}

        res = await db['users'].update_one(query, filter)

        if res is not None:
            return True

    return False


def get_confirm_router(database, authenticator) -> APIRouter:
    router = APIRouter()

    @router.get('/{token}')
    async def confirm_mail(token: str, request: Request):
        res = await database['confirmations'].find_one({'token': token})

        if res is None:
            raise HTTPException(status_code=400, detail='Token not valid')

        # TODO: refactor this due to changed _id from ObjectId to UUID
        delta = (datetime.utcnow() - (
            res['_id'].generation_time).replace(tzinfo=None)).total_seconds()

        if res is None:
            raise HTTPException(status_code=400, detail='Token not valid')
        elif delta > 3600 * 24:
            database['confirmations'].delete_one({'token': token})

            raise HTTPException(status_code=400, detail='Token has expired')

        query = {'id': res['id']}
        document = {'$set': {'is_confirmed': True}}

        res_user = await database['users'].update_one(query, document)

        if res_user.acknowledged:
            await database['confirmations'].delete_one({'token': token})
            user = await database['users'].find_one({'id': res['id']})

            await activate_user(user)

        return {}

    return router
