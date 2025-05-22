from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class ZoomMeetingCreate(BaseModel):
    topic: str = None
    # start_time: datetime = None
    # duration: Optional[int] = None  # minutes
    # type: Optional[int] = None  # 2 = Scheduled meeting

class ZoomMeetingResponse(BaseModel):
    message: str
    meeting_url: str
    start_url: str
