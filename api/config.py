from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    jwt_secret: str
    admin_email: str
    reset_secret: str
    database_url: str
    smtp_username: str
    smtp_password: str
    smtp_server: str
    smtp_port: int
    smtp_tls: bool
    smtp_ssl: bool

    class Config:
        env_file = '.env'
