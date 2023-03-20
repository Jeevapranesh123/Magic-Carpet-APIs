from pydantic import BaseModel


class ResBaseModel(BaseModel):
    status: str = "success"
    message: str = "Request Successful"
