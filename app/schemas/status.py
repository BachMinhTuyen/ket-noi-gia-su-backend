from pydantic import BaseModel
from typing import Optional
import uuid

class StatusCreate(BaseModel):
    code: str
    name: str

    class Config:
        from_attributes = True

class StatusOut(BaseModel):
    statusId: uuid.UUID
    code: Optional[str]
    name: Optional[str]

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    code: Optional[str]
    name: Optional[str]

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedStatusResponse(BaseModel):
    pagination: PaginationMeta
    data: list[StatusOut]

    class Config:
        from_attributes = True