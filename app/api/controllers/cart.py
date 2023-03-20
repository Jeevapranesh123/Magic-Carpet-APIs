from app.db.mongodb import AsyncIOMotorClient
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from app.models.cart import ItemAddReq, ItemAddRes, ItemDeleteReq
from app.crud import cart as cart_crud

async def add_to_cart(
    new_cart_item: ItemAddReq,
    Authorize: AuthJWT,
    db: AsyncIOMotorClient,
):

    if not await cart_crud.check_item_exists(new_cart_item, db):
        raise HTTPException(
            status_code=404,
            detail="Item Not Found in Inventory",
        )
    if not await cart_crud.check_quantity(new_cart_item, db):
        raise HTTPException(
            status_code=422,
            detail="Quantity not available",
        )
    
    uuid = Authorize.get_jwt_subject()
    if await cart_crud.add_to_cart(new_cart_item, uuid, db):
        return {
            "status":"success",
            "message":"Item Added to Cart"
        }
    

async def delete_from_cart(
        delete_obj: ItemDeleteReq,
        Authorize: AuthJWT,
        db: AsyncIOMotorClient
):
    uuid = Authorize.get_jwt_subject()
    if await cart_crud.delete_from_cart(delete_obj.item_id, uuid, db):
        return {
            "status": "success",
            "message": "Item Deleted from Cart"
        }