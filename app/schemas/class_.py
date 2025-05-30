from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
import uuid

class ClassSearchInput(BaseModel):
    keyword: str
    userId: Optional[uuid.UUID] = None
    limit: Optional[int] = 10

class ClassCreate(BaseModel):
    className_vi: Optional[str] = None
    className_en: Optional[str] = None
    tutorId: Optional[uuid.UUID] = None
    createdBy: uuid.UUID
    subjectId: uuid.UUID
    studyType: Optional[str] = None
    startDate: Optional[datetime] = None
    sessions: Optional[int] = None
    tuitionFee: Optional[Decimal] = None
    description: Optional[str] = None
    maxStudents: Optional[int] = None
    status: uuid.UUID

    class Config:
        from_attributes = True

class ClassOut(BaseModel):
    classId: uuid.UUID
    className_vi: Optional[str] = None
    className_en: Optional[str] = None
    tutorId: Optional[uuid.UUID] = None
    createdBy: uuid.UUID
    subjectId: uuid.UUID
    studyType: Optional[str] = None
    startDate: Optional[datetime] = None
    sessions: Optional[int] = None
    tuitionFee: Optional[Decimal] = None
    description: Optional[str] = None
    maxStudents: Optional[int] = None
    status: uuid.UUID

    class Config:
        from_attributes = True

class ClassUpdate(BaseModel):
    className_vi: Optional[str] = None
    className_en: Optional[str] = None
    tutorId: Optional[uuid.UUID] = None
    subjectId: Optional[uuid.UUID] = None
    studyType: Optional[str] = None
    startDate: Optional[datetime] = None
    sessions: Optional[int] = None
    tuitionFee: Optional[Decimal] = None
    description: Optional[str] = None
    maxStudents: Optional[int] = None
    status: Optional[uuid.UUID] = None

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedClassResponse(BaseModel):
    pagination: PaginationMeta
    data: list[ClassOut]

    class Config:
        from_attributes = True

class MatchingClassResult(BaseModel):
    class_: ClassOut
    distance_km: float
    similarity: float
    matching_score: float

class MatchingClassResponse(BaseModel):
    results: Optional[List[MatchingClassResult]] = None
    message: Optional[str] = None



class ClassRegistrationOut(BaseModel):
    registrationId: uuid.UUID
    classId: uuid.UUID
    studentId: uuid.UUID
    registrationDate: Optional[datetime] = None

class ClassRegistrationCreate(BaseModel):
    classId: uuid.UUID
    studentId: uuid.UUID
    registrationDate: datetime

class PaginatedClassRegistrationResponse(BaseModel):
    pagination: PaginationMeta
    data: list[ClassRegistrationOut]

    class Config:
        from_attributes = True