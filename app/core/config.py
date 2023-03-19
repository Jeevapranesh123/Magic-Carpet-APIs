import logging
from glob import glob
from os import environ as env
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, HttpUrl, validator

load_dotenv(".env")


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: List = [
        "*",
    ]

    PROJECT_NAME: str = env.get("PROJECT_NAME")
    PROJECT_DESCRIPTION: str = env.get("PROJECT_DESCRIPTION")
    API_ROOT_PATH: str = env.get("API_ROOT_PATH", "")

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if v is not None and len(v) == 0:
    #         return None
    #     return v

    MONGODB_URL: str = env.get("MONGODB_URL")
    MONGO_USERS_COLLECTION_NAME: str = "users"
    MONGO_BOOKS_COLLECTION_NAME: str = "courses"
    MONGO_CART_COLLECTION_NAME: str = "chapters"
    MONGO_ORDERS_COLLECTION_NAME: str = "categories"
    MONGO_PROD_DATABASE: str = env.get("MONGO_PROD_DATABASE")
    # print(MONGO_PROD_DATABASE)

    class Config:
        case_sensitive = True


public_key = env.get("JWT_PUBLIC_KEY", None)
if public_key is None:
    with open("public.pem", mode="rb") as public_pem:
        public_key = public_pem.read()

private_key = env.get("JWT_PRIVATE_KEY", None)
if private_key is None:
    with open("private.pem", mode="r") as private_pem:
        private_key = private_pem.read()


class AuthJWTSettings(BaseSettings):
    authjwt_algorithm: str = "RS512"
    authjwt_public_key: str = public_key
    authjwt_private_key: str = private_key


class HealthCheckEndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/ping") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(HealthCheckEndpointFilter())

settings = Settings()
auth_jwt_settings = AuthJWTSettings()
env_with_secrets = env
