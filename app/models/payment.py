from sqlalchemy import Column, String, ForeignKey, DECIMAL, TIMESTAMP, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime, timezone
import uuid

class PaymentMethod(Base):
    __tablename__ = 'PaymentMethod'
    methodId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    methodName = Column(String(50), nullable=False)
    description = Column(Text)
    isActive = Column(Boolean, default=False)
    logoUrl = Column(Text)


class Payment(Base):
    __tablename__ = 'Payment'
    paymentId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registrationId = Column(UUID(as_uuid=True), ForeignKey('ClassRegistration.registrationId'), nullable=False)
    amount = Column(DECIMAL(10, 2))
    paidAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    methodId = Column(UUID(as_uuid=True), ForeignKey('PaymentMethod.methodId'), nullable=False)
    status = Column(UUID(as_uuid=True), ForeignKey('PaymentStatus.statusId'), nullable=False)
    
    status_relation = relationship("PaymentStatus", back_populates="payments")