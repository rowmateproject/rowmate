from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# setup
from setup.init import setup_translations

# router
from router.poll import get_poll_router
from router.stat import get_stats_router
from router.language import get_language_router
from router.boat import get_boats_router, get_boat_router
from router.event import get_events_router, get_event_router
from router.subscription import get_subscription_router
from router.confirm import get_confirm_router
from router.manage import get_manage_router
from router.lookup import get_lookup_router
from router.theme import get_themes_router
from router.auth import get_auth_router
from router.mail import get_mail_router

# hooks
from hooks.register import on_after_register
from hooks.forgot import on_after_forgot_password

# dependencies
from app import api_user, settings, jwt_auth, user_db, db


# intialize
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
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
    get_confirm_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/auth/confirm',
    tags=['auth']
)


app.include_router(
    api_user.get_register_router(on_after_register),
    prefix='/auth',
    tags=['auth']
)


app.include_router(
    api_user.get_reset_password_router(
        settings.reset_secret,
        after_forgot_password=on_after_forgot_password,
        reset_password_token_lifetime_seconds=3600
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
    get_mail_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/mail',
    tags=['mails']
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
    get_boat_router(
        database=db,
        authenticator=api_user
    ),
    prefix='/boat',
    tags=['boats']
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
