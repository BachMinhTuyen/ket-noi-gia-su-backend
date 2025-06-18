from sqlalchemy import Column, ForeignKey, Integer, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime, timezone
import uuid

class Evaluation(Base):
    __tablename__ = 'Evaluation'
    evaluationId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    classId = Column(UUID(as_uuid=True), ForeignKey('Class.classId'), nullable=False)
    fromUserId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    toUserId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    criteria1 = Column(Integer)
    criteria2 = Column(Integer)
    criteria3 = Column(Integer)
    comment = Column(Text)
    evaluationDate = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    
    from_user = relationship("User", back_populates="sent_evaluations", foreign_keys=[fromUserId])
    to_user = relationship("User", back_populates="received_evaluations", foreign_keys=[toUserId])
