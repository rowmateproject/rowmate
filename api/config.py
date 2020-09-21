from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    reset_secret: str
    database_url: str
    admin_email: str
    app_name: str

    class Config:
        env_file = '.env'
