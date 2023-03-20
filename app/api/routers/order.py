from app.db.mongodb import AsyncIOMotorClient, get_database
from fastapi import APIRouter, HTTPException, Depends, Response
from app.api.controllers import order as order_controller
from app.models.order import Checkout

from fastapi_jwt_auth import AuthJWT

router = APIRouter()


@router.post("/checkout", response_model="")
async def create_order(
    checkout_obj: Checkout,
    Authorize: AuthJWT = Depends(),
    db: AsyncIOMotorClient = Depends(get_database),
):
    res = await order_controller.checkout(checkout_obj,Authorize, db)
    pass


@router.post("/update", response_model="")
async def update_order():
    pass


# TODO Prohibit deletion of orders, instead mark them as cancelled
@router.post("/delete", response_model="")
async def delete_order():
    pass


@router.get("/get", response_model="")
async def get_order():
    pass


@router.get("/get_all", response_model="")
async def get_all_orders():
    pass


@router.get("/get_all_by_user", response_model="")
async def get_all_orders_by_user():
    pass
