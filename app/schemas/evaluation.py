from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# Evaluation
class EvaluationOut(BaseModel):
    evaluationId: Optional[uuid.UUID] = None
    classId: Optional[uuid.UUID] = None
    fromUserId: Optional[uuid.UUID] = None
    toUserId: Optional[uuid.UUID] = None
    criteria1: Optional[int] = None
    criteria2: Optional[int] = None
    criteria3: Optional[int] = None
    comment: Optional[str] = None
    evaluationDate: Optional[datetime] = None

    class Config:
        from_attributes = True

class EvaluationCreate(BaseModel):
    classId: uuid.UUID
    fromUserId: uuid.UUID
    toUserId: uuid.UUID
    criteria1: Optional[int] = None
    criteria2: Optional[int] = None
    criteria3: Optional[int] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True

class EvaluationUpdate(BaseModel):
    criteria1: Optional[int] = None
    criteria2: Optional[int] = None
    criteria3: Optional[int] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedEvaluationResponse(BaseModel):
    pagination: PaginationMeta
    data: list[EvaluationOut]

    class Config:
        from_attributes = True
