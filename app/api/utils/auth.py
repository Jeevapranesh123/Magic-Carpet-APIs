from fastapi_jwt_auth import AuthJWT


async def create_access_token(
    Authorize: AuthJWT, uuid: str, expires_time: int = 3600
) -> str:
    # user_claims = await get_token_user_claims(uuid, mongodb)
    return Authorize.create_access_token(subject=uuid, expires_time=expires_time)


async def create_refresh_token(Authorize: AuthJWT, uuid: str) -> str:
    # user_claims = await get_token_user_claims(uuid, mongodb)
    return Authorize.create_refresh_token(subject=uuid)


async def create_access_and_refresh_token(Authorize: AuthJWT, uuid: str) -> dict:
    access_token = await create_access_token(Authorize, uuid=uuid)

    # TODO: Save refresh token in database
    refresh_token = await create_refresh_token(Authorize, uuid=uuid)
    return {"access_token": access_token, "refresh_token": refresh_token}
