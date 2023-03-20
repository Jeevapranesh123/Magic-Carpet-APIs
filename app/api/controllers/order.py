from app.db.mongodb import AsyncIOMotorClient
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from app.models.order import Checkout, CheckOutFinal
from app.crud import order as order_crud

async def checkout(
    checkout_obj: Checkout,
    Authorize: AuthJWT,
    db: AsyncIOMotorClient,
):
    Authorize.jwt_required()
    
    #Verify Address
    #Verify Payment method, if online, verify payment gateway
    # await order_crud.verify_cart_identity(checkout_obj, Authorize, db)

    data = checkout_obj.dict()
    data['cart_uuid'] = Authorize.get_jwt_subject()
    data['delivery_charge'] = 0
    print(data)
    checkout_obj_final = CheckOutFinal(**data)
    await order_crud.checkout(checkout_obj_final, db)