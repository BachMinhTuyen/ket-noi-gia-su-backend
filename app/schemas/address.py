from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid

class AddressOut(BaseModel):
    addressId: Optional[uuid.UUID] = None
    userId: Optional[uuid.UUID] = None
    classId: Optional[uuid.UUID] = None
    requestId: Optional[uuid.UUID] = None
    province: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    street: Optional[str] = None
    fullAddress: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None

    class Config:
        from_attributes = True

class AddressCreate(BaseModel):
    userId: Optional[uuid.UUID] = None
    classId: Optional[uuid.UUID] = None
    requestId: Optional[uuid.UUID] = None
    fullAddress: Optional[str] = None

    class Config:
        from_attributes = True

class AddressUpdate(BaseModel):
    fullAddress: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedAddressResponse(BaseModel):
    pagination: PaginationMeta
    data: list[AddressOut]

    class Config:
        from_attributes = True