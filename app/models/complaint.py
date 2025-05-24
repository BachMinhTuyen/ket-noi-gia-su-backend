from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime, timezone

class ComplaintType(Base):
    __tablename__ = 'ComplaintType'
    complaintTypeId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    description = Column(Text)

class Complaint(Base):
    __tablename__ = 'Complaint'
    complaintId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('User.userId'))
    complaintTypeId = Column(UUID(as_uuid=True), ForeignKey('ComplaintType.complaintTypeId'))
    title = Column(String(100))
    content = Column(Text)
    resolutionNote = Column(Text)
    status = Column(String(50))
    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="complaints")
