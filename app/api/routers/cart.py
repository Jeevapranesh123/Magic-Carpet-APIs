from app.db.mongodb import AsyncIOMotorClient, get_database
from fastapi import APIRouter, HTTPException, Depends, Response

router = APIRouter()


@router.post("/add", response_model="")
async def add_to_cart():
    pass


@router.post("/delete", response_model="")
async def delete_from_cart():
    pass


@router.post("/update", response_model="")
async def update_cart():
    pass


@router.get("/get", response_model="")
async def get_cart():
    pass


@router.get("/get_all", response_model="")
async def get_all_carts():
    pass
