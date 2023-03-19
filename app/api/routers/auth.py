from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.auth import RegisterReqModel, RegisterResModel
from app.crud.auth import check_existing_email, check_existing_mobile
from fastapi import APIRouter, HTTPException, Depends, Response
from app.api.controllers import auth as auth_controller


router = APIRouter()


@router.post("/register", response_model=RegisterResModel)
async def register(
    register_obj: RegisterReqModel,
    response: Response,
    db: AsyncIOMotorClient = Depends(get_database),
):
    res = await auth_controller.register(register_obj, db)
    return res
