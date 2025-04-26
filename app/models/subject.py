from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Subject(Base):
    __tablename__ = 'Subject'
    subjectId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subjectName_vi = Column(String(100))
    subjectName_en = Column(String(100))
    description = Column(String(255))