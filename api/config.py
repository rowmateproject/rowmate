from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = 'Rowmate'
    client_id: str
    client_key: str
    jwt_secret: str
    admin_email: str
    cors_origin: str
    backend_url: str
    frontend_url: str
    reset_secret: str
    database_url: str
    smtp_username: str
    smtp_password: str
    smtp_server: str
    smtp_port: int = 465
    smtp_tls: bool = False
    smtp_ssl: bool = True

    class Config:
        env_file = '.env'
