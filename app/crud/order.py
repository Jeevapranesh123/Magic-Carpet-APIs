from app.core.config import settings
from app.db.mongodb import AsyncIOMotorClient
from fastapi import HTTPException
from app.models.order import CheckOutFinal
from uuid import uuid4
from datetime import datetime

import pprint



async def checkout(
    checkout_obj:CheckOutFinal,
    db: AsyncIOMotorClient,
):

    cart = await db[settings.MONGO_PROD_DATABASE][
        settings.MONGO_CART_COLLECTION_NAME
    ].find_one({"id": checkout_obj.cart_id})

    if not cart:
        raise HTTPException(status_code=400, detail="Cart not found")
    
    if not cart["items"]:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    order = {
        "uuid": str(uuid4()).split("-")[0],
        "cart_uuid": checkout_obj.cart_uuid,
        "order_total": 0,
        "delivery_charges": checkout_obj.delivery_charges,
        "delivery_address": checkout_obj.address,
        "payment_method": checkout_obj.payment_method,
        "items":[],
        "order_status": "placed",
        "order_date": datetime.now(),
        "delivery_date": "",
        "delivery_status": "pending",
    }
    for item in cart["items"]:
        product = await db[settings.MONGO_PROD_DATABASE][
            settings.MONGO_BOOKS_COLLECTION_NAME
        ].find_one({"id": item["item_id"]})

        if product["quantity"] < item["quantity"]:
            raise HTTPException(status_code=422, detail="Quantity not available for some items")
        
        order["order_total"] += product["price"] * item["quantity"]
        order["items"].append({
            "item_id": item["item_id"],
            "name": item["name"],
            "quantity": item["quantity"],
            "price": product["price"],
        })

        order["order_total"] += checkout_obj.delivery_charges


    pprint.pprint(order)