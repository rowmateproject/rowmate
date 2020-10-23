from fastapi import APIRouter, HTTPException, Request, Response, Form, status

from httpx_oauth.oauth2 import BaseOAuth2

from fastapi_users.db import BaseUserDatabase
from fastapi_users.models import UD, BaseUserDB, BaseOAuthAccount
from fastapi_users.password import generate_password, get_password_hash
from fastapi_users.router.common import run_handler

from typing import Callable, Optional, Type, cast

from google.oauth2 import id_token
from google.auth.transport import requests

import httpx

# auth
from auth.user import CustomAuthenticator

# app
from app import settings


def get_oauth_router(
    oauth_client: BaseOAuth2,
    user_db: BaseUserDatabase[BaseUserDB],
    user_db_model: Type[BaseUserDB],
    authenticator: CustomAuthenticator,
    state_secret: str,
    redirect_url: str,
    after_register: Optional[Callable[[UD, Request], None]] = None
) -> APIRouter:
    router = APIRouter()

    @router.post('/callback')
    async def login_google(request: Request,
                           response: Response,
                           code: str = Form(...),
                           client_id: str = Form(...),
                           redirect_uri: str = Form(...),
                           response_type: str = Form(...),
                           grant_type: str = Form(...),
                           code_verifier: str = Form(...)):
        url = 'https://oauth2.googleapis.com/token'

        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': settings.client_key,
            'code_verifier': code_verifier,
            'redirect_uri': redirect_uri,
            'grant_type': grant_type
        }

        r = httpx.post(url, json=data).json()
        token = r['id_token']

        try:
            oauth_user = id_token.verify_oauth2_token(
                token, requests.Request(), client_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid authentication'
            )

        # 'email_verified': True,
        # 'locale': 'de',

        user = await user_db.get_by_oauth_account(
            oauth_client.name, oauth_user['sub'])

        new_oauth_account = BaseOAuthAccount(
            oauth_name=oauth_client.name,
            expires_at=oauth_user['exp'],
            account_email=oauth_user['email'],
            access_token=r['access_token'],
            account_id=oauth_user['sub']
        )

        if not user:
            user = await user_db.get_by_email(oauth_user['email'])

            if user:
                # Link account
                user.oauth_accounts.append(new_oauth_account)
                await user_db.update(user)
            else:
                # Create account
                password = generate_password()

                user = user_db_model(
                    email=oauth_user['email'],
                    hashed_password=get_password_hash(password),
                    oauth_accounts=[new_oauth_account],
                )

                await user_db.create(user)

                if after_register:
                    await run_handler(after_register, user, request)
        else:
            # Update oauth
            updated_oauth_accounts = []

            for oauth_account in user.oauth_accounts:
                if oauth_account.account_id == oauth_user['sub']:
                    updated_oauth_accounts.append(new_oauth_account)
                else:
                    updated_oauth_accounts.append(oauth_account)

            user.oauth_accounts = updated_oauth_accounts
            await user_db.update(user)

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Must activate account'
            )
        elif not user.is_confirmed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Account not confirmed'
            )
        elif not user.is_accepted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Account not accepted'
            )

        # Authenticate
        for backend in authenticator.backends:
            if backend.name == 'jwt':
                return await backend.get_login_response(
                    cast(BaseUserDB, user), response
                )

    return router
