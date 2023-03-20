from app.db.mongodb import AsyncIOMotorClient, get_database
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi_jwt_auth import AuthJWT
from app.models.cart import ItemAddReq, ItemAddRes, ItemDeleteReq
from app.api.controllers import cart as cart_controller

router = APIRouter()


@router.post("/add", response_model="")
async def add_to_cart(
    new_cart_item: ItemAddReq,
    Authorize: AuthJWT = Depends(),
    db: AsyncIOMotorClient = Depends(get_database),
):
    Authorize.jwt_required()

    res = await cart_controller.add_to_cart(new_cart_item, Authorize,db)
    return res


@router.post("/delete", response_model="")
async def delete_from_cart(
    delete_obj: ItemDeleteReq,
    Authorize: AuthJWT = Depends(),
    db: AsyncIOMotorClient = Depends(get_database),
):
    Authorize.jwt_required()

    res = await cart_controller.delete_from_cart(delete_obj, Authorize, db)
    return res


@router.post("/update", response_model="")
async def update_cart():
    pass


@router.get("/get", response_model="")
async def get_cart():
    pass


@router.get("/get_all", response_model="")
async def get_all_carts():
    pass
