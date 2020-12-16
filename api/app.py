from fastapi_users.db import MongoDBUserDatabase
from fastapi_mail import FastMail, ConnectionConfig
from motor.motor_asyncio import AsyncIOMotorClient

# config
from config import Settings

# models
from models.user import User, UserDB, UserCreate, UserUpdate

# classes
from auth.user import Authentication
from auth.api import APIUsers
from pymongo import TEXT

# settings
settings = Settings()

# client
client = AsyncIOMotorClient(
    settings.database_url, uuidRepresentation='standard'
)

# database
db = client['rowmate']
db['templates'].create_index([('ngrams', TEXT)], name='templates_ngrams_index')
db['questions'].create_index([('ngrams', TEXT)], name='questions_ngrams_index')
db['events'].create_index([('ngrams', TEXT)], name='events_ngrams_index')

user_db = MongoDBUserDatabase(UserDB, db['users'])    

jwt_auth = Authentication(
    secret=settings.jwt_secret,
    lifetime_seconds_refresh=50000,
    lifetime_seconds=3600
)

api_user = APIUsers(
    user_db,
    [jwt_auth],
    User,
    UserCreate,
    UserUpdate,
    UserDB
)


smtp_config = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_username,
    MAIL_PASSWORD=settings.smtp_password,
    MAIL_SERVER=settings.smtp_server,
    MAIL_PORT=settings.smtp_port,
    MAIL_TLS=settings.smtp_tls,
    MAIL_SSL=settings.smtp_ssl,
    MAIL_FROM=settings.smtp_username
)
# initialize
mail = FastMail(smtp_config)
