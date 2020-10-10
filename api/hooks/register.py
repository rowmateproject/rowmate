from fastapi import Request
from fastapi_mail import MessageSchema

import secrets

# models
from models.user import UserDB

# dependencies
from app import db, mail, settings


async def on_after_register(user: UserDB, request: Request):
    token = secrets.token_urlsafe(32)

    await db['confirmations'].insert_one({'id': user.id, 'token': token})

    if await db['invited'].find_one({'email': user.email}) is not None:
        print(await db['users'].update_one(
            {'id': user.id}, {'$set': {'is_accepted': True}}))

    token_url = f'{settings.frontend_url}/confirm/{token}'

    message = MessageSchema(
        subject='Welcome to rowmate.org',
        receipients=[user.email],
        body=f'Hi {user.name},\n\nthis is your registration mail with your verification link:\n\n{token_url}\n\nBest regards,\nrowmate.org'
    )

    await mail.send_message(message)

    return {'detail': 'Verification mail has been sent'}
