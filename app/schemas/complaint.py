from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
import uuid

# Complaint
class ComplaintOut(BaseModel):
    complaintId: Optional[uuid.UUID] = None
    userId: Optional[uuid.UUID] = None
    complaintTypeId: Optional[uuid.UUID] = None
    title: Optional[str] = None
    content: Optional[str] = None
    resolutionNote: Optional[str] = None
    status: Optional[str] = None
    createdAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class ComplaintCreate(BaseModel):
    userId: uuid.UUID
    complaintTypeId: uuid.UUID
    title: Optional[str] = None
    content: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class ComplaintUpdate(BaseModel):
    complaintTypeId: Optional[uuid.UUID] = None
    title: Optional[str] = None
    content: Optional[str] = None
    resolutionNote: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedComplaintResponse(BaseModel):
    pagination: PaginationMeta
    data: list[ComplaintOut]

    class Config:
        from_attributes = True


# Complaint Type
class ComplaintTypeOut(BaseModel):
    complaintTypeId: Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ComplaintTypeCreate(BaseModel):
    name: str = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ComplaintTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedComplaintTypeResponse(BaseModel):
    pagination: PaginationMeta
    data: list[ComplaintTypeOut]

    class Config:
        from_attributes = True
