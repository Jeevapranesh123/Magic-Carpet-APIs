from app.db.mongodb import AsyncIOMotorClient, get_database
from fastapi import APIRouter, HTTPException, Depends, Response
from app.api.controllers import books as books_controller
from app.models.books import NewBook, BookCreateRes



router = APIRouter()


@router.post("/add", response_model=BookCreateRes)
async def add_book(
    new_book: NewBook,
    response: Response,
    db: AsyncIOMotorClient = Depends(get_database),
):
    
    res = await books_controller.add_book(new_book, db)
    return res
    


@router.post("/delete", response_model="")
async def delete_book():
    pass


@router.post("/update", response_model="")
async def update_book():
    pass


@router.get("/get", response_model="")
async def get_book(
    id: str,
    db: AsyncIOMotorClient = Depends(get_database),
):
    res = await books_controller.get_book(id, db)
    return res



@router.get("/get_all", response_model="")
async def get_all_books(
    db: AsyncIOMotorClient = Depends(get_database),
):
    res = await books_controller.get_all_books(db)
    return res
