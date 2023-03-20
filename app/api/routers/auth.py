from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.auth import RegisterReqModel, RegisterResModel, LoginReqModel, LoginResModel
from app.crud.auth import check_existing_email, check_existing_mobile
from fastapi import APIRouter, HTTPException, Depends, Response
from app.api.controllers import auth as auth_controller
from fastapi_jwt_auth import AuthJWT


router = APIRouter()


@router.post("/register", response_model=RegisterResModel)
async def register(
    register_obj: RegisterReqModel,
    response: Response,
    Authorize: AuthJWT = Depends(),
    db: AsyncIOMotorClient = Depends(get_database),
):
    res = await auth_controller.register(register_obj,Authorize, db)
    response.status_code = 201
    return res

@router.post("/login", response_model="")
async def login(
    login_obj: LoginReqModel,
    response: Response,
    Authorize: AuthJWT = Depends(),
    db: AsyncIOMotorClient = Depends(get_database),
):
    
    res = await auth_controller.login(login_obj, Authorize, db)
    response.status_code = 200
    return res