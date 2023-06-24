import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

_host = os.environ.get('MYSQL_HOST')
_database = os.environ.get('MYSQL_DATABASE')
_user = os.environ.get('MYSQL_USER')
_password = os.environ.get('MYSQL_PASSWORD')

class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = f"mysql+aiomysql://{_user}:{_password}@{_host}:3306/{_database}"
    READER_DB_URL: str = f"mysql+aiomysql://{_user}:{_password}@{_host}:3306/{_database}"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://{_user}:{_password}@{_host}:3306/{_database}"
    READER_DB_URL: str = f"mysql+aiomysql://{_user}:{_password}@{_host}:3306/{_database}"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://{_user}:{_password}@{_host}:3306/{_database}"
    READER_DB_URL: str = f"mysql+aiomysql://{_user}:{_password}@{_host}:3306/{_database}"


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = f"mysql+aiomysql://{_user}:{_password}@{_host}:3306/{_database}"
    READER_DB_URL: str = f"mysql+aiomysql://{_user}:{_password}@{_host}:3306/{_database}"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
