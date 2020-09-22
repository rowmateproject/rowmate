import motor.motor_asyncio

from fastapi import FastAPI, Depends, Request, Response
from fastapi_users import models, FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import JWTAuthentication
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional

import config


class User(models.BaseUser):
    name: Optional[str]


class UserCreate(models.BaseUserCreate):
    name: str


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


client = motor.motor_asyncio.AsyncIOMotorClient(
    config.Settings().database_url, uuidRepresentation='standard'
)

db = client['rowmate']
collection = db['users']


user_db = MongoDBUserDatabase(UserDB, collection)

auth_backends = []
jwt_authentication = JWTAuthentication(
    secret=config.Settings().jwt_secret,
    tokenUrl='/auth/jwt/login',
    lifetime_seconds=3600
)
auth_backends.append(jwt_authentication)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

fastapi_user = Depends(fastapi_users.get_current_active_user)


app = FastAPI()

origins = [
    'http://localhost:3000',
]


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f'User {user.id} has forgot their password. Reset token: {token}')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix='/auth/jwt',
    tags=['auth']
)


app.include_router(
    fastapi_users.get_register_router(),
    prefix='/auth',
    tags=['auth'],
)


app.include_router(
    fastapi_users.get_reset_password_router(
        config.Settings().reset_secret,
        after_forgot_password=on_after_forgot_password,
        reset_password_token_lifetime_seconds=3600
    ),
    prefix='/auth',
    tags=['auth'],
)


app.include_router(
    fastapi_users.get_users_router(),
    prefix='/users',
    tags=['users'],
)


@app.post('/auth/jwt/refresh')
async def refresh_jwt(response: Response, user=fastapi_user):
    return await jwt_authentication.get_login_response(user, response)


@app.get('/')
def hello_world():
    return {'key': 'open'}


@app.get('/protected')
def hello_world_protected(user=fastapi_user):
    return {'key': 'protected'}
