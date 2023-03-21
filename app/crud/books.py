import datetime
import random
import string
from uuid import uuid4
from fastapi_jwt_auth import AuthJWT
from app.db.mongodb import AsyncIOMotorClient
from app.models.books import NewBook, BookInCreate, GetBook

from app.core.config import settings


async def check_existing_book(
    name: str,
    conn: AsyncIOMotorClient,
):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_BOOKS_COLLECTION_NAME
    ].find_one({"name": name})
    if data:
        return True
    return False


async def add_book(new_book: NewBook, conn: AsyncIOMotorClient):
    book_data = new_book.dict()

    # Universally unique identifier is used as book id for now, replace it with meaningful id depending on the use case
    book_data["id"] = str(uuid4()).split("-")[0]
    book_data["added_at"] = datetime.datetime.utcnow()

    new_book = BookInCreate(**book_data)

    res = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_BOOKS_COLLECTION_NAME
    ].insert_one(new_book.dict())

    if res:
        return new_book
    return False


async def get_books(conn: AsyncIOMotorClient):
    data = conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_BOOKS_COLLECTION_NAME
    ].find()

    books = []

    async for book in data:
        books.append(GetBook(**book))

    return books


async def get_book(id: str, conn: AsyncIOMotorClient):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_BOOKS_COLLECTION_NAME
    ].find_one({"id": id})

    if data:
        return GetBook(**data)
    return False
