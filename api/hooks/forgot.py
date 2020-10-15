from fastapi import Request
from fastapi_mail import MessageSchema

# models
from models.user import UserDB

# dependencies
from app import mail, settings


async def on_after_forgot_password(user: UserDB, token: str, request: Request):
    token_url = f'{settings.frontend_url}/reset/{token}'
    signup_url = f'{settings.frontend_url}/signup'

    message = MessageSchema(
        subject=f'{user.name} reset your password',
        recipients=[user.email],
        body=f'Hi {user.name},\n\na new password has been requested for your rowmate account. If you have not made this request, please ignore this email.\n\nIf you need a new password, please confirm the request by visiting the following link within 12 hours.\n\n{token_url}\n\nAfterwards, you can login at {signup_url} with your new password. Your previous password can no longer be used.\n\nBest regards,\napp.rowmate.org'
    )

    res = await mail.send_message(message)

    if res:
        return 'Password reset mail has been sent'
    else:
        return 'Error sending password reset mail'
