from fastapi_users import FastAPIUsers
from fastapi_users.db import BaseUserDatabase
from fastapi_users.authentication.base import BaseAuthentication
from fastapi_users.password import generate_password, get_password_hash
from fastapi_users.models import (
    BaseUser, BaseUserDB, BaseUserCreate, BaseUserUpdate)

from typing import Awaitable, Sequence, Type
from typing_extensions import Protocol

from pydantic import EmailStr

# auth
from auth.user import CustomAuthenticator


class APIUsers(FastAPIUsers):
    authenticator: CustomAuthenticator

    def __init__(
            self, db: BaseUserDatabase,
            auth_backends: Sequence[BaseAuthentication],
            user_model: Type[BaseUser],
            user_create_model: Type[BaseUserCreate],
            user_update_model: Type[BaseUserUpdate],
            user_db_model: Type[BaseUserDB]):
        self.db = db
        self.authenticator = CustomAuthenticator(auth_backends, db)

        self._user_model = user_model
        self._user_db_model = user_db_model
        self._user_create_model = user_create_model
        self._user_update_model = user_update_model
        self._user_db_model = user_db_model

        self.create_user = get_create_user(db, user_db_model)
        self.verify_user = get_verify_user(db)
        self.get_user = get_get_user(db)

        self.get_current_user = self.authenticator.get_current_user
        self.get_current_active_user = (
            self.authenticator.get_current_active_user
        )
        self.get_current_superuser = self.authenticator.get_current_superuser
        self.get_optional_current_user = (
            self.authenticator.get_optional_current_user
        )
        self.get_optional_current_active_user = (
            self.authenticator.get_optional_current_active_user
        )
        self.get_optional_current_superuser = (
            self.authenticator.get_optional_current_superuser
        )

class UserAlreadyExists(Exception):
    pass


class UserNotExists(Exception):
    pass


class UserAlreadyVerified(Exception):
    pass


class CreateUserProtocol(Protocol):
    def __call__(
        self,
        user: BaseUserCreate,
        safe: bool = False,
        is_active: bool = None,
        is_verified: bool = None,
    ) -> Awaitable[BaseUserDB]:
        pass


def get_create_user(
    user_db: BaseUserDatabase[BaseUserDB],
    user_db_model: Type[BaseUserDB],
) -> CreateUserProtocol:
    async def create_user(
        user: BaseUserCreate,
        safe: bool = False,
        is_active: bool = None,
        is_verified: bool = None,
    ) -> BaseUserDB:
        existing_user = await user_db.get_by_email(user.email)

        if existing_user is not None:
            raise UserAlreadyExists()

        hashed_password = get_password_hash(user.password)
        user_dict = (
            user.create_update_dict() if safe else user.create_update_dict_superuser()
        )
        db_user = user_db_model(**user_dict, hashed_password=hashed_password)
        return await user_db.create(db_user)

    return create_user


class VerifyUserProtocol(Protocol):
    def __call__(self, user: BaseUserDB) -> Awaitable[BaseUserDB]:
        pass


def get_verify_user(
    user_db: BaseUserDatabase[BaseUserDB],
) -> VerifyUserProtocol:
    async def verify_user(user: BaseUserDB) -> BaseUserDB:
        if user.is_verified:
            raise UserAlreadyVerified()

        user.is_verified = True
        return await user_db.update(user)

    return verify_user


class GetUserProtocol(Protocol):
    def __call__(self, user_email: EmailStr) -> Awaitable[BaseUserDB]:
        pass


def get_get_user(
    user_db: BaseUserDatabase[BaseUserDB],
) -> GetUserProtocol:
    async def get_user(user_email: EmailStr) -> BaseUserDB:
        if not (user_email == EmailStr(user_email)):
            raise UserNotExists()

        user = await user_db.get_by_email(user_email)

        if user is None:
            raise UserNotExists()

        return user

    return get_user
