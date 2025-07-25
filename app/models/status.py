from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class PaymentStatus(Base):
    __tablename__ = "PaymentStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    payments = relationship("Payment", back_populates="status_relation", lazy="selectin")

class ScheduleStatus(Base):
    __tablename__ = "ScheduleStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    schedules = relationship("Schedule", back_populates="status_relation", lazy="selectin")

class StudentRequestStatus(Base):
    __tablename__ = "StudentRequestStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    requests = relationship("StudentRequest", back_populates="status_relation", lazy="selectin")

class TutorApplicationStatus(Base):
    __tablename__ = "TutorApplicationStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    applications = relationship("TutorApplication", back_populates="status_relation", lazy="selectin")

class ClassStatus(Base):
    __tablename__ = "ClassStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    classes = relationship("Class", back_populates="status_relation", lazy="selectin")