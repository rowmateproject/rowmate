from fastapi_users.db import BaseUserDatabase
from fastapi_users.models import (
    BaseUser, BaseUserDB, BaseUserCreate, BaseUserUpdate)
from fastapi_users.password import get_password_hash

from datetime import datetime
from typing import Optional, Dict
from pydantic import UUID4

import asyncio
import pytest


viviane_password_hash = get_password_hash('viviane')
angharad_password_hash = get_password_hash('angharad')
guinevere_password_hash = get_password_hash('guinevere')
lancelot_password_hash = get_password_hash('lancelot')


class User(BaseUser):
    is_active: bool = False
    is_accepted: bool = False
    is_confirmed: bool = False
    birth: Optional[datetime]
    locale: Optional[str]
    phone: Optional[str]
    name: Optional[str]
    avatar: Dict


class UserCreate(BaseUserCreate):
    name: str


class UserUpdate(User, BaseUserUpdate):
    birth: datetime
    avatar: dict
    locale: str
    phone: str


class UserDB(User, BaseUserDB):
    pass


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture
def user() -> UserDB:
    return UserDB(
        email='king.arthur@camelot.bt',
        hashed_password=guinevere_password_hash,
        is_confirmed=False,
        is_accepted=False,
        is_active=True,
        avatar={}
    )


@pytest.fixture
def inactive_user() -> UserDB:
    return UserDB(
        email='percival@camelot.bt',
        hashed_password=angharad_password_hash,
        is_active=False,
        is_confirmed=False,
        is_accepted=False,
        avatar={}
    )


@pytest.fixture
def confirmed_user() -> UserDB:
    return UserDB(
        email='percival@camelot.bt',
        hashed_password=angharad_password_hash,
        is_active=False,
        is_confirmed=True,
        is_accepted=False,
        avatar={}
    )


@pytest.fixture
def accepted_user() -> UserDB:
    return UserDB(
        email='percival@camelot.bt',
        hashed_password=angharad_password_hash,
        is_active=False,
        is_confirmed=False,
        is_accepted=True,
        avatar={}
    )


@pytest.fixture
def superuser() -> UserDB:
    return UserDB(
        email='merlin@camelot.bt',
        hashed_password=viviane_password_hash,
        is_superuser=True,
        is_confirmed=False,
        is_accepted=False,
        is_active=False,
        avatar={}
    )


@pytest.fixture
def mock_user_db(user, inactive_user, superuser) -> BaseUserDatabase:
    class MockUserDatabase(BaseUserDatabase[UserDB]):
        async def get(self, id: UUID4) -> Optional[UserDB]:
            if id == user.id:
                return user
            if id == inactive_user.id:
                return inactive_user
            if id == confirmed_user.id:
                return confirmed_user
            if id == accepted_user.id:
                return accepted_user
            if id == superuser.id:
                return superuser
            return None

        async def get_by_email(self, email: str) -> Optional[UserDB]:
            lower_email = email.lower()
            if lower_email == user.email.lower():
                return user
            if lower_email == inactive_user.email.lower():
                return inactive_user
            if lower_email == confirmed_user.email.lower():
                return confirmed_user
            if lower_email == accepted_user.email.lower():
                return accepted_user
            if lower_email == superuser.email.lower():
                return superuser
            return None

        async def create(self, user: UserDB) -> UserDB:
            return user

        async def update(self, user: UserDB) -> UserDB:
            return user

        async def delete(self, user: UserDB) -> None:
            pass

    return MockUserDatabase(UserDB)
