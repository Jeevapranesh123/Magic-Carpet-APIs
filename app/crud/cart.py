from app.db.mongodb import AsyncIOMotorClient
from fastapi import HTTPException
from app.models.cart import ItemAddReq, Items

from app.core.config import settings

from uuid import uuid4


async def check_item_exists(new_cart_item: ItemAddReq, conn: AsyncIOMotorClient):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_BOOKS_COLLECTION_NAME
    ].find_one({"id": new_cart_item.item_id})

    if not data:
        return False

    return True


async def check_quantity(new_cart_item: ItemAddReq, conn: AsyncIOMotorClient):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_BOOKS_COLLECTION_NAME
    ].find_one({"id": new_cart_item.item_id})
    print(new_cart_item.quantity)
    if data["quantity"] < new_cart_item.quantity:
        return False

    return True


async def add_to_cart(
    new_cart_item: ItemAddReq,
    uuid: str,
    conn: AsyncIOMotorClient,
):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_CART_COLLECTION_NAME
    ].find_one({"uuid": uuid})

    product = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_BOOKS_COLLECTION_NAME
    ].find_one({"id": new_cart_item.item_id})

    new_item = {}
    new_item["item_id"] = product["id"]
    new_item["name"] = product["name"]
    new_item["quantity"] = new_cart_item.quantity
    # new_item["price"] = product["price"]

    item = Items(**new_item)

    if data:
        if await conn[settings.MONGO_PROD_DATABASE][
            settings.MONGO_CART_COLLECTION_NAME
        ].find_one({"uuid": uuid, "items.item_id": new_cart_item.item_id}):
            await conn[settings.MONGO_PROD_DATABASE][
                settings.MONGO_CART_COLLECTION_NAME
            ].update_one(
                {"uuid": uuid, "items.item_id": new_cart_item.item_id},
                {"$inc": {"items.$.quantity": new_cart_item.quantity}},
            )
            return True
        res = await conn[settings.MONGO_PROD_DATABASE][
            settings.MONGO_CART_COLLECTION_NAME
        ].update_one({"uuid": uuid}, {"$push": {"items": item.dict()}})
        if res:
            return True
        return False
    else:
        data = {
            # Universally unique identifier is used as cart id for now, replace it with meaningful id depending on the use case
            "id": str(uuid4()).split("-")[0],
            "uuid": uuid,
            "items": [item.dict()],
        }
        res = await conn[settings.MONGO_PROD_DATABASE][
            settings.MONGO_CART_COLLECTION_NAME
        ].insert_one(data)
        if res:
            return True
        return False


async def delete_from_cart(
    item_id: str,
    uuid: str,
    conn: AsyncIOMotorClient,
):
    data = await conn[settings.MONGO_PROD_DATABASE][
        settings.MONGO_CART_COLLECTION_NAME
    ].find_one({"uuid": uuid})

    if data:
        res = await conn[settings.MONGO_PROD_DATABASE][
            settings.MONGO_CART_COLLECTION_NAME
        ].update_one({"uuid": uuid}, {"$pull": {"items": {"item_id": item_id}}})
        if res:
            return True
        return False
    else:
        return False
