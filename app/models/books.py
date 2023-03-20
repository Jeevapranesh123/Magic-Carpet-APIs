from typing import Any, Dict, List, Optional
from datetime import datetime
from app.models.res_base import ResBaseModel
from pydantic import BaseModel, root_validator


class NewBook(BaseModel):
    name:str
    author:str
    price:int
    quantity:int = 10
    image:str = None # Image url from S3 or any other cloud storage


class BookInCreate(NewBook):
    id: str
    added_at: datetime 

class BookCreateRes(BookInCreate):
    pass

class GetBook(BookInCreate):
    pass

class GetBooks(BaseModel):
    total: int
    books: List[GetBook]
