from app.db.mongodb import AsyncIOMotorClient
from fastapi import HTTPException
from app.models.books import *
from app.crud import books as books_crud


async def add_book(new_book: NewBook, db: AsyncIOMotorClient):
    if await books_crud.check_existing_book(new_book.name, db):
        raise HTTPException(
            status_code=422,
            detail="Book Already exists",
        )

    data = await books_crud.add_book(new_book, db)

    book = BookCreateRes(**data.dict())
    return book


async def get_all_books(db: AsyncIOMotorClient):
    data = await books_crud.get_books(db)
    book_res = {"total": len(data), "books": data}
    return book_res


async def get_book(id: str, db: AsyncIOMotorClient):
    data = await books_crud.get_book(id, db)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found",
        )
    return data
