from fastapi import Depends, Response, HTTPException
from fastapi_users.db import BaseUserDatabase
from fastapi_users.authentication.base import BaseAuthentication
from fastapi_users.authentication import (
    JWTAuthentication, Authenticator, name_to_variable_name)
from fastapi_users.models import BaseUserDB

from makefun import with_signature
from inspect import Signature, Parameter
from typing import Optional, Sequence

# utils
from utils.jwt import generate_jwt


class AuthModel(BaseAuthentication):
    lifetime_seconds_refresh: int


class Authentication(AuthModel, JWTAuthentication):
    token_audience: str = 'jwt:auth'

    def __init__(self,
                 secret: str,
                 lifetime_seconds: int,
                 lifetime_seconds_refresh: int,
                 name: str = 'jwt'):
        super().__init__(name, lifetime_seconds)
        self.lifetime_seconds_refresh = lifetime_seconds_refresh

    async def generate_access_token(self, user: BaseUserDB) -> str:
        data = {'user_id': str(user.id), 'aud': self.token_audience}
        token = generate_jwt(data, self.secret, self.lifetime_seconds)

        return token

    async def generate_refresh_token(self, user: BaseUserDB) -> str:
        data = {'user_id': str(user.id), 'aud': self.token_audience}
        token = generate_jwt(data, self.secret, self.lifetime_seconds_refresh)

        return token

    async def get_login_response(self, user: BaseUserDB, response: Response):
        access_token = await self.generate_access_token(user)
        refresh_token = await self.generate_refresh_token(user)

        return {
            'name': user.name,
            'phone': user.phone,
            'birth': user.birth,
            'avatar': user.avatar,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'is_confirmed': user.is_confirmed,
            'refresh_token': refresh_token,
            'access_token': access_token,
            'token_type': 'bearer'
        }

    async def get_refresh_response(self, user: BaseUserDB, response: Response):
        access_token = await self.generate_access_token(user)

        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }


class CustomAuthenticator(Authenticator):
    backends: Sequence[BaseAuthentication]
    user_db: BaseUserDatabase

    def __init__(self,
                 backends: Sequence[BaseAuthentication],
                 user_db: BaseUserDatabase):
        self.backends = backends
        self.user_db = user_db

        parameters = [Parameter(
            name=name_to_variable_name(backend.name),
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default=Depends(backend.scheme)
        ) for backend in self.backends]

        signature = Signature(parameters)

        @with_signature(signature, func_name='get_optional_current_user')
        async def get_optional_current_user(*args, **kwargs):
            return await self.authenticate(*args, **kwargs)

        @with_signature(signature, func_name='get_optional_current_active_user')
        async def get_optional_current_active_user(*args, **kwargs):
            user = await get_optional_current_user(*args, **kwargs)

            if not user or not user.is_active:
                return None

            return user

        @with_signature(signature, func_name='get_optional_current_superuser')
        async def get_optional_current_superuser(*args, **kwargs):
            user = await get_optional_current_active_user(*args, **kwargs)

            if not user or not user.is_superuser:
                return None

            return user

        @with_signature(signature, func_name='get_current_user')
        async def get_current_user(*args, **kwargs):
            user = await get_optional_current_user(*args, **kwargs)

            if user is None:
                raise HTTPException(status_code=403,
                                    detail='You do not have the permission')

            return user

        @with_signature(signature, func_name='get_current_active_user')
        async def get_current_active_user(*args, **kwargs):
            user = await get_optional_current_active_user(*args, **kwargs)

            if user is None:
                raise HTTPException(status_code=403,
                                    detail='You do not have the permission')

            return user

        @with_signature(signature, func_name='get_current_superuser')
        async def get_current_superuser(*args, **kwargs):
            user = await get_optional_current_active_user(*args, **kwargs)

            if user is None:
                raise HTTPException(status_code=403,
                                    detail='You do not have the permission')

            if not user.is_superuser:
                raise HTTPException(status_code=403,
                                    detail='You need to be superuser')

            return user

        self.get_current_user = get_current_user
        self.get_current_active_user = get_current_active_user
        self.get_optional_current_active_user = get_optional_current_active_user
        self.get_optional_current_superuser = get_optional_current_superuser
        self.get_optional_current_user = get_optional_current_user
        self.get_current_superuser = get_current_superuser

    async def authenticate(self, *args, **kwargs) -> Optional[BaseUserDB]:
        # print(dir(self), args, kwargs)

        for backend in self.backends:
            token: str = kwargs[name_to_variable_name(backend.name)]

            if token and token != 'undefined':
                user = await backend(token, self.user_db)

                if user is not None:
                    return user

        # TODO: this needs to be refactored due refresh token response
        raise HTTPException(status_code=401, detail='Token has expired')
