import datetime
import random
import string
from uuid import uuid4
from fastapi_jwt_auth import AuthJWT
from app.db.mongodb import AsyncIOMotorClient
from app.models.auth import RegisterReqModel, RegisterResModel, User
from fastapi import HTTPException

from app.core.config import settings

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



async def check_existing_email(
    email: str,
    conn: AsyncIOMotorClient,
):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_USERS_COLLECTION_NAME
    ].find_one({"email": email})
    if data:
        return True
    return False


async def check_existing_mobile(
    mobile: int,
    conn: AsyncIOMotorClient,
):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_USERS_COLLECTION_NAME
    ].find_one({"mobile": mobile})
    if data:
        return True
    return False


async def register(register_obj, conn: AsyncIOMotorClient):
    print("Hello")
    data = {
        "uuid": str(uuid4()).replace("-", ""),
        "name": register_obj.name,
        "email": register_obj.email,
        "mobile": register_obj.mobile,
        "password": get_password_hash(register_obj.password),
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
    }
    res = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_USERS_COLLECTION_NAME
    ].insert_one(data)
    data.pop("_id")
    if res:
        return data
    return False


async def login(login_obj, conn: AsyncIOMotorClient):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_USERS_COLLECTION_NAME
    ].find_one({"email": login_obj.email})
    if data:
        if verify_password(login_obj.password, data["password"]):
            user = User(**data)
            return user
        raise HTTPException(
            status_code=401, detail="Incorrect email or password"
        )
    raise HTTPException(
        status_code=401, detail="Incorrect email or password"
    )

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)