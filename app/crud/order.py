from app.core.config import settings
from app.db.mongodb import AsyncIOMotorClient
from fastapi import HTTPException
from app.models.order import CheckOutFinal, Order
from uuid import uuid4
from datetime import datetime

import pprint


async def verify_cart_identity(checkout_obj, Authorize, db):
    cart = await db[settings.MONGO_PROD_DATABASE][
        settings.MONGO_CART_COLLECTION_NAME
    ].find_one({"uuid": Authorize.get_jwt_subject()})

    if cart:
        if not cart["id"] == checkout_obj.cart_id:
            raise HTTPException(
                status_code=403, detail="This cart does not belong the current user"
            )


async def checkout(
    checkout_obj: CheckOutFinal,
    db: AsyncIOMotorClient,
):
    cart = await db[settings.MONGO_PROD_DATABASE][
        settings.MONGO_CART_COLLECTION_NAME
    ].find_one({"uuid": checkout_obj.cart_uuid})

    if not cart:
        raise HTTPException(status_code=400, detail="Cart not found")

    if not cart["items"]:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = {
        "id": str(uuid4()).split("-")[0],
        "cart_uuid": checkout_obj.cart_uuid,
        "cart_id": checkout_obj.cart_id,
        "order_total": 0,
        "delivery_charges": checkout_obj.delivery_charges,
        "delivery_address": checkout_obj.address,
        "payment_method": checkout_obj.payment_method,
        "items": [],
        "order_status": "placed",
        "order_date": datetime.now(),
        "delivery_date": checkout_obj.delivery_date,
        "delivery_status": "pending",
    }
    for item in cart["items"]:
        product = await db[settings.MONGO_PROD_DATABASE][
            settings.MONGO_BOOKS_COLLECTION_NAME
        ].find_one({"id": item["item_id"]})

        if product["quantity"] < item["quantity"]:
            raise HTTPException(
                status_code=422, detail="Quantity not available for some items"
            )

        order["order_total"] += product["price"] * item["quantity"]
        order["items"].append(
            {
                "item_id": item["item_id"],
                "name": item["name"],
                "quantity": item["quantity"],
                "price": product["price"],
            }
        )

        order["order_total"] += checkout_obj.delivery_charges

    # TODO Implementing transaction here as there are multiple dependent operations
    if await db[settings.MONGO_PROD_DATABASE][
        settings.MONGO_ORDERS_COLLECTION_NAME
    ].insert_one(order):
        for item in cart["items"]:
            await db[settings.MONGO_PROD_DATABASE][
                settings.MONGO_BOOKS_COLLECTION_NAME
            ].update_one(
                {"id": item["item_id"]},
                {"$inc": {"quantity": -item["quantity"]}},
            )

            await db[settings.MONGO_PROD_DATABASE][
                settings.MONGO_CART_COLLECTION_NAME
            ].update_one(
                {"uuid": checkout_obj.cart_uuid},
                {"$pull": {"items": {"item_id": item["item_id"]}}},
            )

        new_order = Order(**order)
        return new_order

    else:
        raise HTTPException(status_code=500, detail="Something went wrong")
