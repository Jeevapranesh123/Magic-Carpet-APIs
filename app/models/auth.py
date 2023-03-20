from typing import Any, Dict, List, Optional
from app.models.res_base import ResBaseModel
from pydantic import BaseModel, root_validator


class RegisterReqModel(BaseModel):
    name: str
    email: str = None
    password: str
    mobile: int


class RegisterResModel(ResBaseModel):
    tokens: Optional[dict]
    user_details: dict

class User(BaseModel):
    uuid: str
    name: str
    email: str
    mobile: int


class LoginReqModel(BaseModel):
    email: str
    password: str

class LoginResModel(ResBaseModel):
    tokens: Optional[dict]
