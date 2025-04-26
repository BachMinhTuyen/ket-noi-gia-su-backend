from sqlalchemy import Column, String, ForeignKey, Date, Time, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Schedule(Base):
    __tablename__ = 'Schedule'
    scheduleId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    classId = Column(UUID(as_uuid=True), ForeignKey('Class.classId'), nullable=False)
    zoomUrl = Column(Text)
    zoomMeetingId = Column(String(50))
    zoomPassword = Column(String(50))
    date = Column(Date)
    startTime = Column(Time)
    endTime = Column(Time)
    status = Column(UUID(as_uuid=True), ForeignKey('ScheduleStatus.statusId'), nullable=False)
    
    class_relation = relationship("Class", back_populates="schedules")
    status_relation = relationship("ScheduleStatus", back_populates="schedules")