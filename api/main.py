import motor.motor_asyncio
import secrets
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi_users import models, FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import JWTAuthentication
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

import config
import re
mailregex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class UserList(BaseModel):
    mails: List[str] = []
    sendmail: bool = False

class User(models.BaseUser):
    name: Optional[str]
    is_active: bool = False
    is_accepted: bool = False
    mail_confirmed: bool = False


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


async def activateuser(user: UserDB):
    if user['is_accepted'] and user['mail_confirmed']:
        if await collection.find_one_and_update({ 'id': user['id'] }, { '$set': { 'is_active': True }}) is not None:
            return True

    return False


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f'User {user.id} has forgot their password. Reset token: {token}')


async def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")
    token = secrets.token_urlsafe(16)
    result = db.confirmations.insert_one({ 'id': user.id, 'token': token })
    print(f"Created Mail-Verification-Token: {token}")
    if await db.invited.find_one({ 'email': user.email }) is not None:
        print(await collection.find_one_and_update({ 'id': user.id }, { '$set': { 'is_accepted': True }}))
    else:
        print("User hasn't been invited over E-Mail")


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

@app.get("/confirm/{token}")
async def confirm_mail(token: str, request: Request):
    user = await db.confirmations.find_one({ 'token': token })

    if user is None:
        raise HTTPException(status_code=400, detail="Token not valid")
    elif (datetime.now(timezone.utc) - user['_id'].generation_time).total_seconds() > 3600*24:
        db.confirmations.delete_one({ 'token': token })
        raise HTTPException(status_code=400, detail="Token expired")

    if await collection.find_one_and_update({ 'id': user['id'] },  { '$set': { 'mail_confirmed': True }}) is not None:
        db.confirmations.delete_one({ 'token': token })
        user = await collection.find_one({ 'id': user['id'] })

        await activateuser(user)

    return {}



@app.post("/users/invite")
async def invitemails(users: UserList, user=fastapi_user):
    mails = []
    if user.is_superuser is False:
        for mail in users.mails:
            if not re.search(mail,mailregex):
                mails.append({ 'email': mail })

        inserted = await db.invited.insert_many(mails)
        if len(inserted.inserted_ids) == len(mails):
            return { "status": "ok", "details": "Inserted all emails"}
        else:
            return { "details": "Not all emails have been inserted"}

    else:
        raise HTTPException(status_code=403, detail="Not Admin")




@app.get('/')
def hello_world():
    return {'key': 'open'}


@app.get('/protected')
def hello_world_protected(user=fastapi_user):
    return {'key': 'protected'}
