from sqlalchemy import Column, String, ForeignKey, Integer, TIMESTAMP, DECIMAL, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Class(Base):
    __tablename__ = 'Class'
    classId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    createdBy = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    className_vi = Column(String(100))
    className_en = Column(String(100))
    subjectId = Column(UUID(as_uuid=True), ForeignKey('Subject.subjectId'), nullable=False)
    tutorId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    studyType = Column(String(20))
    startDate = Column(Date)
    sessions = Column(Integer)
    tuitionFee = Column(DECIMAL(10, 2))
    description = Column(Text)
    maxStudents = Column(Integer)
    status = Column(UUID(as_uuid=True), ForeignKey('ClassStatus.statusId'), nullable=False)
    
    created_by = relationship("User", back_populates="created_classes", foreign_keys=[createdBy])
    tutor = relationship("User", back_populates="tutor_classes", foreign_keys=[tutorId])
    status_relation = relationship("ClassStatus", back_populates="classes")
    schedules = relationship("Schedule", back_populates="class_relation")
    class_registrations = relationship("ClassRegistration", back_populates="class_relation")

class ClassRegistration(Base):
    __tablename__ = 'ClassRegistration'
    registrationId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    classId = Column(UUID(as_uuid=True), ForeignKey('Class.classId'), nullable=False)
    studentId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    registrationDate = Column(TIMESTAMP(timezone=True))
    
    class_relation = relationship("Class", back_populates="class_registrations")
    student = relationship("User", back_populates="class_registrations")