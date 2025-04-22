from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class PaymentStatus(Base):
    __tablename__ = "PaymentStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

class ScheduleStatus(Base):
    __tablename__ = "ScheduleStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

class StudentRequestStatus(Base):
    __tablename__ = "StudentRequestStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

class TutorApplicationStatus(Base):
    __tablename__ = "TutorApplicationStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

class ClassStatus(Base):
    __tablename__ = "ClassStatus"
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
