from sqlalchemy import Column, String, ForeignKey, Text, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class StudentRequest(Base):
    __tablename__ = 'StudentRequest'
    requestId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    studentId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    subjectId = Column(UUID(as_uuid=True), ForeignKey('Subject.subjectId'), nullable=False)
    studyType = Column(String(20))
    preferredSchedule = Column(Text)
    tuitionFee = Column(DECIMAL(10, 2))
    location = Column(String(100))
    description = Column(Text)
    status = Column(UUID(as_uuid=True), ForeignKey('StudentRequestStatus.statusId'), nullable=False)
    
    student = relationship("User", back_populates="student_requests")
    status_relation = relationship("StudentRequestStatus", back_populates="requests")