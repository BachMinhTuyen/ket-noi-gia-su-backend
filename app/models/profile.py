from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class StudentProfile(Base):
    __tablename__ = 'StudentProfile'
    studentId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    gradeLevel = Column(String(20))
    learningGoals = Column(Text)
    preferredStudyTime = Column(Text)
    description = Column(String(255))
    
    user = relationship("User", back_populates="student_profile")

class TutorProfile(Base):
    __tablename__ = 'TutorProfile'
    tutorId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    degree = Column(String(100))
    certificate = Column(String(100))
    experience = Column(String(255))
    description = Column(String(255))
    introVideoUrl = Column(Text)
    isApproved = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="tutor_profile")