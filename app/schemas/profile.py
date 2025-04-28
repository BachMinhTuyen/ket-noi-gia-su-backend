from pydantic import BaseModel
from typing import Optional
import uuid

# Student Profile Schemas
class StudentProfileIn(BaseModel):
    gradeLevel: Optional[str]
    learningGoals: Optional[str]
    preferredStudyTime: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True

class StudentProfileOut(BaseModel):
    studentId: uuid.UUID
    gradeLevel: Optional[str]
    learningGoals: Optional[str]
    preferredStudyTime: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True

#Tutor Profile Schemas
class TutorProfileIn(BaseModel):
    degree: Optional[str] = None
    certificate: Optional[str] = None
    experience: Optional[str] = None
    description: Optional[str] = None
    introVideoUrl: Optional[str] = None

    class Config:
        from_attributes = True

class TutorProfileOut(BaseModel):
    tutorId: uuid.UUID
    degree: Optional[str] = None
    certificate: Optional[str] = None
    experience: Optional[str] = None
    description: Optional[str] = None
    introVideoUrl: Optional[str] = None

    class Config:
        from_attributes = True