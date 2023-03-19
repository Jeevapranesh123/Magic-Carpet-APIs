from app.db.mongodb import AsyncIOMotorClient, get_database
from fastapi import APIRouter, HTTPException, Depends, Response


router = APIRouter()


@router.post("/add", response_model="")
async def add_book():
    pass


@router.post("/delete", response_model="")
async def delete_book():
    pass


@router.post("/update", response_model="")
async def update_book():
    pass


@router.get("/get", response_model="")
async def get_book():
    pass


@router.get("/get_all", response_model="")
async def get_all_books():
    pass
