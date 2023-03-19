from app.models.auth import RegisterReqModel, RegisterResModel
from app.db.mongodb import AsyncIOMotorClient
from app.crud.auth import check_existing_email, check_existing_mobile
from fastapi import HTTPException
# from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.crud import auth as auth_crud

async def register(
        register_obj: RegisterReqModel,
        db: AsyncIOMotorClient
):
    
    if await check_existing_email(register_obj.email, db):
        raise HTTPException(
            status_code=400,
            detail="Email Already exists",
        )    

    print("Hi")
    if await check_existing_mobile(register_obj.mobile, db):
        raise HTTPException(
            status_code=400,
            detail="Mobile Already exists",
        )

    data = await auth_crud.register(register_obj, db)
    return data