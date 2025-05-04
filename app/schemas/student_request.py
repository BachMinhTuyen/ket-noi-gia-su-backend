from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid

class StudentRequestOut(BaseModel):
    requestId: uuid.UUID
    studentId: uuid.UUID
    subjectId: uuid.UUID
    studyType: Optional[str] = None
    preferredSchedule: Optional[str] = None
    tuitionFee: Optional[Decimal] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: uuid.UUID 

    class Config:
        from_attributes = True

class StudentRequestCreate(BaseModel):
    studentId: uuid.UUID
    subjectId: uuid.UUID
    studyType: Optional[str] = None
    preferredSchedule: Optional[str] = None
    tuitionFee: Optional[Decimal] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: uuid.UUID 

    class Config:
        from_attributes = True

class StudentRequestUpdate(BaseModel):
    studentId: Optional[uuid.UUID] = None
    subjectId: Optional[uuid.UUID] = None
    studyType: Optional[str] = None
    preferredSchedule: Optional[str] = None
    tuitionFee: Optional[Decimal] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedClassResponse(BaseModel):
    pagination: PaginationMeta
    data: list[StudentRequestOut]

    class Config:
        from_attributes = True 