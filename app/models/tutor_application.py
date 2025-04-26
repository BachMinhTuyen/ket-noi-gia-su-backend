from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class TutorApplication(Base):
    __tablename__ = 'TutorApplication'
    applicationId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tutorId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    requestId = Column(UUID(as_uuid=True), ForeignKey('StudentRequest.requestId'), nullable=False)
    applicationDate = Column(DateTime)
    status = Column(UUID(as_uuid=True), ForeignKey('TutorApplicationStatus.statusId'), nullable=False)
    
    tutor = relationship("User", back_populates="tutor_applications")
    status_relation = relationship("TutorApplicationStatus", back_populates="applications")