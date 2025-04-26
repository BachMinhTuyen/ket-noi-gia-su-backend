from sqlalchemy import Column, String, ForeignKey, DECIMAL  
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Address(Base):
    __tablename__ = 'Address'
    addressId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('User.userId'))
    classId = Column(UUID(as_uuid=True), ForeignKey('Class.classId'))
    requestId = Column(UUID(as_uuid=True), ForeignKey('StudentRequest.requestId'))
    province = Column(String(50))
    district = Column(String(50))
    ward = Column(String(50))
    street = Column(String(100))
    fullAddress = Column(String(255))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    
    user = relationship("User", back_populates="addresses")
