import motor.motor_asyncio
import datetime as dt
import secrets

from backports.zoneinfo import ZoneInfo
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.models import (
    BaseUser, BaseUserDB, BaseUserCreate, BaseUserUpdate)
from fastapi_users.authentication import JWTAuthentication
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, validator
from typing import Optional, List, Any, Dict

from uuid import UUID
import config
import re
import pymongo

mail_address_pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class Authentication(JWTAuthentication):
    async def get_login_response(self, user: BaseUserDB, response: Response) -> Any:
        access_token = await self._generate_token(user)

        return {
            'name': user.name,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'is_confirmed': user.is_confirmed,
            'access_token': access_token,
            'token_type': 'bearer'
        }


class User(BaseUser):
    name: Optional[str]
    phone: Optional[str]
    birth: Optional[datetime]
    is_active: bool = False
    is_accepted: bool = False
    is_confirmed: bool = False
    avatar: Dict = {
        'isCircle': True,
        'circleColor': '#6fb8e0',
        'accessoriesType': 'Blank',
        'clotheType': 'Hoodie',
        'clotheColor': 'PastelBlue',
        'eyebrowType': 'Default',
        'eyeType': 'Happy',
        'facialHairColor': 'Brown',
        'facialHairType': 'Blank',
        'graphicType': 'Diamond',
        'hairColor': 'Brown',
        'mouthType': 'Default',
        'skinColor': 'Tanned',
        'topType': 'LongHairBob'
    }


class UserCreate(BaseUserCreate):
    name: str


class UserUpdate(User, BaseUserUpdate):
    phone: str
    birth: datetime

    @validator('birth', pre=True, always=True)
    def set_birth_date(cls, v):
        print(v)
        # d = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f%z')

        return v


class UserDB(User, BaseUserDB):
    pass


class UserList(BaseModel):
    mails: List[str] = []
    sendmail: bool = False


client = motor.motor_asyncio.AsyncIOMotorClient(
    config.Settings().database_url, uuidRepresentation='standard'
)


db = client['rowmate']
collection = db['users']
origins = ['http://localhost:3000']


user_db = MongoDBUserDatabase(UserDB, collection)

auth_backends = []
jwt_authentication = Authentication(
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f'User {user.id} has forgot their password. Reset token: {token}')


async def activate_user(user: UserDB):
    if user['is_accepted'] and user['is_confirmed']:
        if await collection.update_one({'id': user['id']}, {'$set': {'is_active': True}}) is not None:
            return True

    return False


async def on_after_register(user: UserDB, request: Request):
    print(f'User {user.id} has registered.')
    token = secrets.token_urlsafe(32)
    db.confirmations.insert_one({'id': user.id, 'token': token})
    print(f'Created mail verification token {token}')

    if await db.invited.find_one({'email': user.email}) is not None:
        print(await collection.update_one({'id': user.id}, {'$set': {'is_accepted': True}}))
    else:
        print('User hasn\'t been invited via Mail')


app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix='/auth/jwt',
    tags=['auth']
)


app.include_router(
    fastapi_users.get_register_router(on_after_register),
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



@app.get('/user/activate/{uuid}')
async def activate_user(uuid: str, request: Request, requser=fastapi_user):
    if requser.is_superuser:
        user = await collection.find_one({'id': UUID(uuid)})
        if await collection.update_one({'id': user['id']}, {'$set': { 'is_active': True, 'is_accepted': True }}) is not None: # accepting the user when user is activated
            return { 'status': 'ok' }
        else:
            raise HTTPException(status_code=404, detail='Update failed')
    else:
        raise HTTPException(status_code=403, detail='You need to be superuser')

@app.get('/user/deactivate/{uuid}')
async def deactivate_user(uuid: str, request: Request, requser=fastapi_user):
    if requser.is_superuser:
        user = await collection.find_one({'id': UUID(uuid)})
        if user is not None:
            if await collection.update_one({ 'id': user['id'] }, { '$set': { 'is_active': False }}) is not None:
                return { 'status': 'ok' }
            else:
                raise HTTPException(status_code=500, detail='Update failed')
        else:
            raise HTTPException(status_code=404, detail='User not found')
    else:
        raise HTTPException(status_code=403, detail='You need to be superuser')


@app.get('/confirm/{token}')
async def confirm_mail(token: str, request: Request):
    user = await db.confirmations.find_one({'token': token})

    if user is None:
        raise HTTPException(status_code=400, detail='Token not valid')
    elif (datetime.now(timezone.utc) - user['_id'].generation_time).total_seconds() > 3600 * 24:
        db.confirmations.delete_one({'token': token})
        raise HTTPException(status_code=400, detail='Token has expired')

    if await collection.update_one({'id': user['id']}, {'$set': {'is_confirmed': True}}) is not None:
        db.confirmations.delete_one({'token': token})
        user = await collection.find_one({'id': user['id']})

        await activate_user(user)

    return {}

@app.post('/users/invite')
async def invite_user(users: UserList, user=fastapi_user):
    mails = []

    if user.is_superuser:
        for mail in users.mails:
            if not re.search(mail, mail_address_pattern):
                mails.append({'email': mail})

        inserted = await db.invited.insert_many(mails)

        if len(inserted.inserted_ids) == len(mails):
            return {'detail': 'Successfully added all email addreesses'}
        else:
            return {'detail': 'Not all email addreesses have been added'}

    else:
        raise HTTPException(status_code=403, detail='You need to be superuser')

@app.get('/dashboard/users')
async def invite_user(user=fastapi_user):

    if user.is_superuser:
        users = []
        for user in await collection.find({}).sort([ ('_id', pymongo.DESCENDING) ]).to_list(length=10000):
            try:
                users.append({
                'created': user['_id'].generation_time,
                'id': str(user['id']),
                'name': user['name'],
                'email': user['email'],
                'is_active': user['is_active'],
                'is_accepted': user['is_accepted'],
                'is_superuser': user['is_superuser'],
                'is_confirmed': user['is_confirmed'],
                'avatar': user['avatar']
                })
            except:
                print("Error")

        return { 'users': users }

    else:
        raise HTTPException(status_code=403, detail='You need to be superuser')

@app.get('/protected')
def hello_world_protected(user=fastapi_user):
    return {'key': 'protected'}
