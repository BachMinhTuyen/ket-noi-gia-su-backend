from pydantic import BaseModel
from typing import Optional
import uuid

class SubjectBase(BaseModel):
    subjectId: uuid.UUID
    subjectName_vi: Optional[str] = None
    subjectName_en: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes  = True

class SubjectCreate(BaseModel):
    subjectName_vi: Optional[str] = None
    subjectName_en: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes  = True

class SubjectOut(BaseModel):
    subjectId: uuid.UUID
    subjectName_vi: Optional[str] = None
    subjectName_en: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes  = True

class SubjectUpdate(BaseModel):
    subjectName_vi: Optional[str] = None
    subjectName_en: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes  = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedSubjectResponse(BaseModel):
    pagination: PaginationMeta
    data: list[SubjectOut]

    class Config:
        from_attributes  = True