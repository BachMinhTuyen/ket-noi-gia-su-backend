from pydantic import BaseModel
from typing import Optional, Any

class MessageResponse(BaseModel):
    message: str

class ResponseWithMessage(BaseModel):
    message: str
    data: Optional[Any] = None