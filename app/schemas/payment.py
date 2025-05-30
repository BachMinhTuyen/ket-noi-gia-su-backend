from pydantic import BaseModel
from fastapi import UploadFile, File
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
import uuid

class PaymentOrderOut(BaseModel):
    paymentId: uuid.UUID
    registrationId: uuid.UUID
    amount: Optional[Decimal] = None
    paidAt: Optional[datetime] = None
    methodId: uuid.UUID
    status: uuid.UUID
    class Config:
        from_attributes = True

class PaymentOrderCreate(BaseModel):
    registrationId: uuid.UUID

    class Config:
        from_attributes = True

class PayOrderData(BaseModel):
    paymentId: uuid.UUID
    methodId: uuid.UUID

    class Config:
        from_attributes = True

class PaymentOrderUpdate(BaseModel):
    amount: Optional[Decimal] = None
    paidAt: Optional[datetime] = None
    methodId: Optional[uuid.UUID] = None
    status: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedPaymentOrderResponse(BaseModel):
    pagination: PaginationMeta
    data: List[PaymentOrderOut]



class PaymentMethodOut(BaseModel):
    methodId: uuid.UUID
    methodName: Optional[str] = None
    description: Optional[str] = None
    isActive: Optional[bool] = False
    logoUrl: Optional[str] = None
    logoPublicId: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateActiveStatus(BaseModel):
    isActive: bool

    class Config:
        from_attributes = True


class PaymentMethodUpdate(BaseModel):
    methodName: Optional[str] = None
    description: Optional[str] = None
    isActive: Optional[bool] = False
    logoUrl: Optional[str] = None
    logoPublicId: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedPaymentMethodResponse(BaseModel):
    pagination: PaginationMeta
    data: List[PaymentMethodOut]
