from fastapi import Depends, APIRouter, Response, HTTPException
from fastapi_users.models import BaseUserDB
from fastapi_users.authentication import Authenticator, BaseAuthentication
from fastapi_users.db import BaseUserDatabase
from fastapi.security import OAuth2PasswordRequestForm
from app import db
from .confirm import activate_user
def get_auth_router(
    backend: BaseAuthentication,
    user_db: BaseUserDatabase[BaseUserDB],
    authenticator: Authenticator
) -> APIRouter:
    router = APIRouter()

    @router.post('/login')
    async def login_jwt(response: Response,
                        credentials: OAuth2PasswordRequestForm = Depends()):
        user = await user_db.authenticate(credentials)

        if user is None:
            raise HTTPException(status_code=400, detail='Wrong credentials')
        elif not user.is_confirmed:
            raise HTTPException(
                status_code=400, detail='Account not confirmed')
        elif not user.is_accepted:
            res = await db['accepted_emails'].count_documents(({'email':user.email}))
            if res > 0:
                document = {'$set': {'is_accepted': True}}
                res_user = await db['users'].update_one({'email':user.email}, document)

                if res_user.acknowledged:
                    await db['accepted_emails'].delete_many({'email':user.email})
                    user = await db['users'].find_one({'email':user.email})

                    await activate_user(user)
                    user = await user_db.authenticate(credentials)
                else:
                    raise HTTPException(status_code=500, detail='Error when updating user')
            else:
                raise HTTPException(status_code=400, detail='Account not accepted')

        elif not user.is_active:
            raise HTTPException(status_code=400, detail='Activate account')
        return await backend.get_login_response(user, response)

    @router.post('/refresh')
    async def refresh_jwt(response: Response, user=Depends(
            authenticator.get_current_active_user)):
        return await backend.get_refresh_response(user, response)

    return router
