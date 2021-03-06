from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx_oauth.clients.google import GoogleOAuth2

# setup
from setup.init import setup_translations

# router
from router.vote import get_vote_router
from router.stat import get_stats_router
from router.google import get_oauth_router
from router.language import get_language_router
from router.organization import get_organization_router
from router.boat import get_boats_router, add_boat_router, delete_boat_router
from router.event import get_events_router, get_event_router
from router.template import get_template_router, get_templates_router
from router.poll import get_poll_router, get_polls_router
from router.subscription import get_subscription_router
from router.confirm import get_confirm_router
from router.manage import get_manage_router
from router.lookup import get_lookup_router
from router.theme import get_themes_router
from router.auth import get_auth_router
from router.chat import add_chat_router
from router.chat import get_user_chats_router
from router.chat import add_chat_message_router
from router.chat import get_chat_messages_router
from router.rowingadvert import get_rowingadverts_router, delete_rowingadvert_router, add_rowingadvert_router, get_rowingadvert_router
from router.acceptedemails import add_emails_router

# hooks
from hooks.register import on_after_register
from hooks.forgot import on_after_forgot_password

# models
from models.user import UserDB

# auth
from auth.user import CustomAuthenticator

# dependencies
from app import api_user, settings, jwt_auth, user_db, db


# intialize
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event('startup')
async def startup():
    await setup_translations(db)


app.include_router(
    get_auth_router(
        backend=jwt_auth,
        user_db=user_db,
        authenticator=api_user
    ),
    prefix='/auth/jwt',
    tags=['auth']
)


app.include_router(
    get_oauth_router(
        oauth_client=GoogleOAuth2(
            settings.client_id,
            settings.client_key
        ),
        user_db=user_db,
        user_db_model=UserDB,
        authenticator=CustomAuthenticator(
            backends=[jwt_auth],
            user_db=user_db
        ),
        state_secret=settings.jwt_secret,
        redirect_url=f'{settings.backend_url}/auth/google/callback',
        after_register=on_after_register
    ),
    prefix='/auth/google',
    tags=['auth']
)


app.include_router(
    get_confirm_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/auth/confirm',
    tags=['auth']
)


app.include_router(
    api_user.get_register_router(
        after_register=on_after_register
    ),
    prefix='/auth',
    tags=['auth']
)


app.include_router(
    api_user.get_reset_password_router(
        settings.reset_secret,
        after_forgot_password=on_after_forgot_password,
        reset_password_token_lifetime_seconds=43200
    ),
    prefix='/auth',
    tags=['auth']
)


app.include_router(
    api_user.get_users_router(),
    prefix='/users',
    tags=['users']
)


app.include_router(
    get_stats_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/stats',
    tags=['stats']
)


app.include_router(
    get_themes_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/theme',
    tags=['themes']
)


app.include_router(
    get_event_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/event',
    tags=['events']
)


app.include_router(
    get_events_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/events',
    tags=['events']
)


app.include_router(
    get_lookup_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/lookup',
    tags=['lookups']
)


app.include_router(
    get_template_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/template',
    tags=['templates']
)


app.include_router(
    get_templates_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/templates',
    tags=['templates']
)


app.include_router(
    get_manage_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/manage',
    tags=['manage']
)


app.include_router(
    get_boats_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/boats',
    tags=['boats']
)


app.include_router(
    add_boat_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/boat',
    tags=['boats']
)


app.include_router(
    delete_boat_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/boat',
    tags=['boats']
)


app.include_router(
    add_chat_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/chat',
    tags=['chats']
)

app.include_router(
    get_user_chats_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/chat',
    tags=['chats']
)


app.include_router(
    add_chat_message_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/chat',
    tags=['chats']
)

app.include_router(
    get_chat_messages_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/chat',
    tags=['chats']
)

app.include_router(
    get_rowingadverts_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/rowingadverts',
    tags=['rowingadverts']
)

app.include_router(
    get_rowingadvert_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/rowingadverts',
    tags=['rowingadverts']
)

app.include_router(
    delete_rowingadvert_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/rowingadverts',
    tags=['rowingadverts']
)

app.include_router(
    add_rowingadvert_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/rowingadverts',
    tags=['rowingadverts']
)

app.include_router(
    get_subscription_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/subscription',
    tags=['subscriptions']
)


app.include_router(
    get_language_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/lang',
    tags=['languages']
)


app.include_router(
    get_poll_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/poll',
    tags=['polls']
)


app.include_router(
    get_polls_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/polls',
    tags=['polls']
)


app.include_router(
    get_vote_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/vote',
    tags=['votes']
)


app.include_router(
    get_organization_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/organization',
    tags=['organizations']
)


app.include_router(
    add_emails_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/accepted-emails',
    tags=['emails']
)
