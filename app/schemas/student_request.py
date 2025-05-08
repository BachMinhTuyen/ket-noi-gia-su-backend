from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
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
    title: Optional[str] = None
    studentCount: Optional[int] = None
    createdAt: Optional[datetime] = None

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
    title: Optional[str] = None
    studentCount: Optional[int] = None

    class Config:
        from_attributes = True

class StudentRequestUpdate(BaseModel):
    subjectId: Optional[uuid.UUID] = None
    studyType: Optional[str] = None
    preferredSchedule: Optional[str] = None
    tuitionFee: Optional[Decimal] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[uuid.UUID] = None
    title: Optional[str] = None
    studentCount: Optional[int] = None

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