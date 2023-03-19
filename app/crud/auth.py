import datetime
import random
import string
from uuid import uuid4
from fastapi_jwt_auth import AuthJWT
from app.db.mongodb import AsyncIOMotorClient
from app.models.auth import RegisterReqModel, RegisterResModel

from app.core.config import settings

async def check_existing_email(email:str, conn: AsyncIOMotorClient,):
    data = await conn[settings.MONGO_PROD_DATABASE][
            settings.MONGO_USERS_COLLECTION_NAME
            ].find_one({"email": email})
    if data:
        return True
    return False

async def check_existing_mobile(mobile:int, conn: AsyncIOMotorClient,):
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
        "password": register_obj.password,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
    }
    res = await conn[settings.MONGO_PROD_DATABASE][
            settings.MONGO_USERS_COLLECTION_NAME
            ].insert_one(data)
    if res:
        register_res = RegisterResModel(**data)
        print(register_res)
        return register_res
    return False
