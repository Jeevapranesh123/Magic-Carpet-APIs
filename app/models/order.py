from typing import Any, Dict, List, Optional
from datetime import datetime
from app.models.res_base import ResBaseModel
from pydantic import BaseModel


class Checkout(BaseModel):
    cart_id: str
    address: str = "XYZ"
    payment_method: str = "COD"


class CheckOutFinal(Checkout):
    cart_uuid: str
    delivery_charges: int = 0
    delivery_date: datetime


class Order(BaseModel):
    id: str
    cart_uuid: str
    cart_id: str
    order_total: int
    delivery_charges: int
    delivery_address: str
    payment_method: str
    items: List
    order_status: str
    order_date: datetime
    delivery_date: datetime
    delivery_status: str


class OrderRes(ResBaseModel):
    details: Order
