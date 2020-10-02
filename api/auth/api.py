from fastapi_users import FastAPIUsers
from fastapi_users.db import BaseUserDatabase
from fastapi_users.authentication.base import BaseAuthentication
from fastapi_users.models import (
    BaseUser, BaseUserDB, BaseUserCreate, BaseUserUpdate)

from typing import Sequence, Type

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
