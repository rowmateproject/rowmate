from fastapi import Depends, APIRouter, Response, HTTPException
from fastapi_users.models import BaseUserDB
from fastapi_users.authentication import Authenticator, BaseAuthentication
from fastapi_users.db import BaseUserDatabase
from fastapi.security import OAuth2PasswordRequestForm


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
        elif not user.is_active:
            raise HTTPException(status_code=400, detail='Activate account')
        elif not user.is_confirmed:
            raise HTTPException(
                status_code=400, detail='Account not confirmed')
        elif not user.is_accepted:
            raise HTTPException(status_code=400, detail='Account not accepted')

        return await backend.get_login_response(user, response)

    @router.post('/refresh',
                 dependencies=[Depends(authenticator.get_current_active_user)])
    async def refresh_jwt(response: Response):
        return await backend.get_refresh_response(authenticator, response)

    return router
