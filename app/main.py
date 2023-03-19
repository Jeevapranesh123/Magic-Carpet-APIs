import inspect
import re
import sys

sys.dont_write_bytecode = True

import uvicorn
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api import router as api_router
from app.core.config import auth_jwt_settings, env_with_secrets, settings
from app.core.errors import (
    authjwt_exception_handler,
    http422_error_handler,
    http_error_handler,
)
from app.db.mongodb_utils import close_mongo_connection, connect_to_mongodb

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0",
        description=settings.PROJECT_DESCRIPTION,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**,\
                where JWT is the access token",
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route, "endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint))
                or re.search("fresh_jwt_required", inspect.getsource(endpoint))
                or re.search("jwt_optional", inspect.getsource(endpoint))
                or re.search("AuthJWT", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {"Bearer Auth": []}
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if "ELASTIC_APM_SERVER_URL" in env_with_secrets:
    try:
        elastic_apm = make_apm_client(
            {
                "SERVICE_NAME": settings.PROJECT_NAME,
                "SERVER_URL": env_with_secrets["ELASTIC_APM_SERVER_URL"],
                "DEBUG": True,
            }
        )
        app.add_middleware(ElasticAPM, client=elastic_apm)
    except Exception as e:
        print(f"Problem Setting Up Elastic APM => {e}")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


app.add_event_handler("startup", connect_to_mongodb)
app.add_event_handler("shutdown", close_mongo_connection)

# set opentracing


@app.on_event("startup")
async def startup():
    # setup_opentracing(app)
    # app.add_middleware(OpentracingMiddleware)
    logger.info("Application started")


@AuthJWT.load_config
def get_config():
    return auth_jwt_settings


app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)
app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

app.include_router(api_router, prefix=settings.API_ROOT_PATH)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=4522,
        log_level="info",
        reload=True,
        workers=1,
    )
