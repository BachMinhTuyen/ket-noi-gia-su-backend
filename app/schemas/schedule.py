from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time
import uuid

class ScheduleOut(BaseModel):
    scheduleId: uuid.UUID
    classId: uuid.UUID
    zoomUrl: Optional[str] = None
    zoomMeetingId: Optional[str] = None
    zoomPassword: Optional[str] = None
    dayStudying: Optional[date] = None
    startTime: Optional[time] = None
    endTime: Optional[time] = None
    status: uuid.UUID

    class Config:
        from_attributes = True

class BulkScheduleCreate(BaseModel):
    classId: uuid.UUID
    weekdays: List[int]  # [0, 1 ,2, 3, 4, 5, 6] là Thứ 2, 3, 4, 5, 6, 7
    startTime: time
    endTime: time

    class Config:
        from_attributes = True

class ScheduleCreate(BaseModel):
    classId: uuid.UUID
    dayStudying: date
    startTime: time
    endTime: time

    class Config:
        from_attributes = True

class ScheduleUpdate(BaseModel):
    zoomUrl: Optional[str] = None
    zoomMeetingId: Optional[str] = None
    zoomPassword: Optional[str] = None
    dayStudying: Optional[date] = None
    startTime: Optional[time] = None
    endTime: Optional[time] = None
    status: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedScheduleResponse(BaseModel):
    pagination: PaginationMeta
    data: list[ScheduleOut]

    class Config:
        from_attributes = True 
