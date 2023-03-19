from typing import Any, Dict, List, Optional
from app.models.res_base import ResBaseModel
from pydantic import BaseModel, root_validator


class RegisterReqModel(BaseModel):
    name: str
    email: str = None
    password: str
    mobile: int


class RegisterResModel(ResBaseModel):
    name: str
    message: str = "User Registered Successfully"
    email: str = None
    mobile: str


class LoginReqModel(BaseModel):
    email: str
    password: str
