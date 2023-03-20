from typing import Any, Dict, List, Optional
from datetime import datetime
from app.models.res_base import ResBaseModel
from pydantic import BaseModel


class Checkout(BaseModel):
    cart_id : str
    address : str = "XYZ"
    payment_method : str = "COD"

class CheckOutFinal(Checkout):
    cart_uuid: str
    delivery_charges: int = 0

