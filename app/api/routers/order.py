from app.db.mongodb import AsyncIOMotorClient, get_database
from fastapi import APIRouter, HTTPException, Depends, Response


router = APIRouter()


@router.post("/create", response_model="")
async def create_order():
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
