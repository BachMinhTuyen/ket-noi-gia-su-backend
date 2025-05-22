from pydantic import BaseModel
from typing import Optional, Any
import uuid

class MessageResponse(BaseModel):
    message: str

class MessageResponseWithId(BaseModel):
    message: str
    id: Optional[uuid.UUID] = None

class ResponseWithMessage(BaseModel):
    message: str
    data: Optional[Any] = None