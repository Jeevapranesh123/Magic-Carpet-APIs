from pydantic import BaseModel


# Base Model for all responses
class ResBaseModel(BaseModel):
    status: str = "success"
    message: str = "Request Successful"
