import motor.motor_asyncio
import secrets

from fastapi import (FastAPI, HTTPException, Depends, Request, Response)
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.models import (
    BaseUser, BaseUserDB, BaseUserCreate, BaseUserUpdate)
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.authentication.base import BaseAuthentication
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict
from uuid import UUID

import pymongo
import config
import jwt
import re

mail_address_pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def generate_jwt(data: dict, secret: str, lifetime_seconds: int) -> str:
    expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
    data['exp'] = expire

    return jwt.encode(data, secret, algorithm='HS256').decode('utf-8')


class AuthModel(BaseAuthentication):
    lifetime_seconds_refresh: int


class Authentication(AuthModel, JWTAuthentication):
    def __init__(self,
                 secret: str,
                 lifetime_seconds: int,
                 lifetime_seconds_refresh: int,
                 name: str = 'jwt'):
        super().__init__(name, lifetime_seconds)
        self.lifetime_seconds_refresh = lifetime_seconds_refresh

    async def generate_access_token(self, user: BaseUserDB) -> str:
        data = {'user_id': str(user.id)}
        token = generate_jwt(data, self.secret, self.lifetime_seconds)

        return token

    async def generate_refresh_token(self, user: BaseUserDB) -> str:
        data = {'user_id': str(user.id)}
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


class User(BaseUser):
    is_active: bool = False
    is_accepted: bool = False
    is_confirmed: bool = False
    birth: Optional[datetime]
    phone: Optional[str]
    name: Optional[str]
    avatar: Dict = {
        'isCircle': True,
        'mouthType': 'Smile',
        'accessoriesType': 'Blank',
        'graphicType': 'Bat',
        'topType': 'Hat',
        'topColor': 'Gray02',
        'clotheType': 'CollarSweater',
        'clotheColor': 'Black',
        'eyeType': 'Wink',
        'eyebrowType': 'Default',
        'facialHairType': 'Blank',
        'facialHairColor': 'Auburn',
        'hairColor': 'Brown',
        'skinColor': 'Yellow',
        'circleColor': '#87CEEB'
    }


class UserCreate(BaseUserCreate):
    name: str


class UserUpdate(User, BaseUserUpdate):
    birth: datetime
    avatar: dict
    phone: str


class UserDB(User, BaseUserDB):
    pass


class UserList(BaseModel):
    mails: List[str] = []
    sendmail: bool = False


class FindUser(BaseModel):
    limit: int = 10
    name: str


class ThemeModel(BaseModel):
    bodyText: str = '#8f9498'
    buttonBackground: str = '#192733'
    buttonText: str = '#ffffff'
    footerBackground: str = '#22619c'
    footerText: str = '#323a5d'
    formBackground: str = '#ffffff'
    formBorder: str = '#a7b0b3'
    formText: str = '#32385d'
    headerBackground: str = '#2852a2'
    imageBackground: str = '#324d5d'
    imageText: str = '#32445d'
    linkText: str = '#3a60d0'
    navBackground: str = '#212225'
    navText: str = '#ffffff'
    pageBackground: str = '#e8e8e8'
    pageText: str = '#26292b'
    saleText: str = '#32465d'
    titleText: str = '#25524f'


client = motor.motor_asyncio.AsyncIOMotorClient(
    config.Settings().database_url, uuidRepresentation='standard'
)


db = client['rowmate']
collection = db['users']
origins = ['http://localhost:3000']


user_db = MongoDBUserDatabase(UserDB, collection)

auth_backends = []
jwt_auth = Authentication(
    secret=config.Settings().jwt_secret,
    lifetime_seconds_refresh=50000,
    lifetime_seconds=3600
)
auth_backends.append(jwt_auth)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

fastapi_user = Depends(fastapi_users.get_current_active_user)
smtp_config = ConnectionConfig(
    MAIL_USERNAME=config.Settings().smtp_username,
    MAIL_PASSWORD=config.Settings().smtp_password,
    MAIL_SERVER=config.Settings().smtp_server,
    MAIL_PORT=config.Settings().smtp_port,
    MAIL_TLS=config.Settings().smtp_tls,
    MAIL_SSL=config.Settings().smtp_ssl
)


app = FastAPI()
fm = FastMail(smtp_config)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/auth/jwt/login')
async def login_jwt(response: Response,
                    req_form: OAuth2PasswordRequestForm = Depends()):
    user = await user_db.authenticate(req_form)

    if user is None:
        raise HTTPException(status_code=400, detail='Wrong credentials')
    elif not user.is_active:
        raise HTTPException(status_code=400, detail='Activate account')
    elif not user.is_confirmed:
        raise HTTPException(status_code=400, detail='Account not confirmed')
    elif not user.is_accepted:
        raise HTTPException(status_code=400, detail='Account not accepted')

    return await jwt_auth.get_login_response(user, response)


@app.post('/auth/jwt/refresh')
async def refresh_jwt(response: Response, user=fastapi_user):
    return await jwt_auth.get_refresh_response(user, response)


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f'User {user.id} has forgot their password. Reset token: {token}')


async def on_after_register(user: UserDB, request: Request):
    token = secrets.token_urlsafe(32)

    await db.confirmations.insert_one({'id': user.id, 'token': token})

    if await db.invited.find_one({'email': user.email}) is not None:
        print(await collection.update_one({'id': user.id}, {'$set': {'is_accepted': True}}))

    message = MessageSchema(
        subject='Welcome to rowmate.org',
        receipients=[user.email],
        body=f'Hi {user.name},\n\nthis is your registration mail with your verification token\n\n{token}\n\nBest regards,\nrowmate.org'
    )

    await fm.send_message(message)

    return {'detail': 'Verification mai has been sent'}


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


async def activate_user(user: UserDB):
    if user['is_accepted'] and user['is_confirmed']:
        if await collection.update_one({'id': user['id']}, {'$set': {'is_active': True}}) is not None:
            return True

    return False


@app.get('/manage/users/activate/{uuid}')
async def activate_user_by_uuid(uuid: str, request: Request, requser=fastapi_user):
    if requser.is_superuser:
        user = await collection.find_one({'id': UUID(uuid)})

        # accepting the user when user is activated
        if await collection.update_one({'id': user['id']}, {'$set': {'is_active': True, 'is_accepted': True}}) is not None:
            return {'status': 'ok'}
        else:
            raise HTTPException(status_code=404, detail='Update failed')
    else:
        raise HTTPException(status_code=403, detail='You need to be superuser')


@app.get('/manage/users/deactivate/{uuid}')
async def deactivate_user(uuid: str, request: Request, requser=fastapi_user):
    if requser.is_superuser:
        user = await collection.find_one({'id': UUID(uuid)})

        if user is not None:
            if await collection.update_one({'id': user['id']}, {'$set': {'is_active': False}}) is not None:
                return {'status': 'ok'}
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


@app.post('/manage/users/invite')
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


@app.get('/manage/users/list')
async def list_users(user=fastapi_user):
    if user.is_superuser:
        sort = [('_id', pymongo.DESCENDING)]
        query = await collection.find({}).sort(sort).to_list(length=10000)
        users = []

        for user in query:
            try:
                users.append({
                    'id': str(user['id']),
                    'name': user['name'],
                    'email': user['email'],
                    'is_active': user['is_active'],
                    'is_accepted': user['is_accepted'],
                    'is_superuser': user['is_superuser'],
                    'is_confirmed': user['is_confirmed'],
                    'created': user['_id'].generation_time,
                    'avatar': user['avatar']
                })
            except Exception as e:
                print(e)

        return {'users': users}
    else:
        raise HTTPException(status_code=403, detail='You need to be superuser')


@app.post('/social/users/find')
async def find_user_by_name_or_mail(req: FindUser, user=fastapi_user):
    sort = [('_id', pymongo.DESCENDING)]
    users = []

    query = await collection.find({
        'name': {'$regex': re.compile(req.name, re.IGNORECASE)},
        'is_active': True
    }).sort(sort).to_list(length=req.limit)

    for q in query:
        try:
            users.append({
                'id': str(q['id']),
                'name': q['name'],
                'email': q['email'],
                'is_active': q['is_active'],
                'created': q['_id'].generation_time,
                'avatar': q['avatar']
            })
        except Exception as e:
            print(e)

    return {'users': users}


@app.get('/theme/default')
async def get_default_theme(theme: ThemeModel = Depends()):
    query = await db['themes'].find_one({}, {'_id': 0})

    if query is not None:
        return query
    else:
        return theme


@app.patch('/theme/default')
async def patch_default_theme(theme: ThemeModel, user=fastapi_user):
    res = await db['themes'].update_one({}, {'$set': dict(theme)}, upsert=True)

    if res.modified_count > 0:
        return {'detail': 'Theme was Successfully updated'}
    else:
        return {'detail': 'Did not update theme propably no changes'}
