from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Notification(Base):
    __tablename__ = 'Notification'
    notificationId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fromUserId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    toUserId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    title_vi = Column(String(100))
    title_en = Column(String(100))
    message_vi = Column(Text)
    message_en = Column(Text)
    type = Column(String(20))
    isRead = Column(Boolean)
    createdAt = Column(TIMESTAMP(timezone=True))
    
    from_user = relationship("User", back_populates="sent_notifications", foreign_keys=[fromUserId])
    to_user = relationship("User", back_populates="received_notifications", foreign_keys=[toUserId])