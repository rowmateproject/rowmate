from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
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
    smtp_port: int
    smtp_tls: bool
    smtp_ssl: bool

    class Config:
        env_file = '.env'
