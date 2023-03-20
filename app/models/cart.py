from typing import Any, Dict, List, Optional
from datetime import datetime
from app.models.res_base import ResBaseModel
from pydantic import BaseModel


class ItemAddReq(BaseModel):
    item_id: str
    quantity: int = 1

class ItemAddRes(BaseModel):
    pass

class ItemDeleteReq(BaseModel):
    item_id: str
    

class Items(BaseModel):
    item_id: str
    name: str
    quantity: int
    price: int

class Cart(BaseModel):
    id: str
    uuid: str
    items: List[Items]

