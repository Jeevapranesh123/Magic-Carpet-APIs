from app.db.mongodb import AsyncIOMotorClient
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from app.crud.auth import check_existing_email, check_existing_mobile
from app.models.auth import *
from app.crud import auth as auth_crud
from app.api.utils import auth as auth_utils


async def register(
    register_obj: RegisterReqModel, Authorize: AuthJWT, db: AsyncIOMotorClient
):
    if await check_existing_email(register_obj.email, db):
        raise HTTPException(
            status_code=422,
            detail="Email Already exists",
        )

    if await check_existing_mobile(register_obj.mobile, db):
        raise HTTPException(
            status_code=422,
            detail="Mobile Already exists",
        )

    user = await auth_crud.register(register_obj, db)
    if user:
        tokens = await auth_utils.create_access_and_refresh_token(
            Authorize=Authorize, uuid=user["uuid"]
        )
    else:
        raise HTTPException(
            status_code=422,
            detail="User Not Registered, Contact Admin",
        )
    print(tokens)
    user = User(**user)

    return RegisterResModel(
        status="success",
        message="User Registered Successfully",
        tokens=tokens,
        user_details=user,
    )


async def login(login_obj: LoginReqModel, Authorize: AuthJWT, db: AsyncIOMotorClient):
    user = await auth_crud.login(login_obj, db)
    if user:
        tokens = await auth_utils.create_access_and_refresh_token(
            Authorize=Authorize, uuid=user.uuid
        )

    return LoginResModel(
        status="success",
        message="User Logged In Successfully",
        tokens=tokens,
    )
