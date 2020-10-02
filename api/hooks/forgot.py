from fastapi import Request

# models
from models.user import UserDB


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f'User {user.id} forgot password Here is the reset token: {token}')
