from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class TutorApplicationOut(BaseModel):
    applicationId: uuid.UUID
    tutorId: uuid.UUID
    requestId: uuid.UUID
    applicationDate: Optional[datetime] = None
    status: uuid.UUID

    class Config:
        from_attributes = True

class TutorApplicationCreate(BaseModel):
    tutorId: uuid.UUID
    requestId: uuid.UUID
    applicationDate: Optional[datetime] = None
    status: uuid.UUID

    class Config:
        from_attributes = True

class TutorApplicationUpdate(BaseModel):
    status: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedClassResponse(BaseModel):
    pagination: PaginationMeta
    data: list[TutorApplicationOut]

    class Config:
        from_attributes = True 