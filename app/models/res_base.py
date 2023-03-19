from pydantic import BaseModel


class ResBaseModel(BaseModel):
    status_code: int = 200
    message: str = "Request Successful"
