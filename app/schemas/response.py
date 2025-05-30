from pydantic import BaseModel
from typing import Optional, Any
import uuid

class MessageResponse(BaseModel):
    message: str

class MessageResponseWithId(BaseModel):
    message: str
    id: Optional[uuid.UUID] = None

class MessageResponseWithIdAndRedirect(BaseModel):
    message: str
    id: Optional[uuid.UUID] = None
    redirect_url: Optional[str] = None

class ResponseWithMessage(BaseModel):
    message: str
    data: Optional[Any] = None

class ResponseWithPaymentMessage(BaseModel):
    status: str
    message: str
    vnp_ResponseCode: Optional[str] = None
    payment_id: Optional[str] = None
    vnp_OrderInfo: Optional[str] = None
    vnp_Amount: Optional[str] = None
    vnp_BankCode: Optional[str] = None
    vnp_PayDate: Optional[str] = None
