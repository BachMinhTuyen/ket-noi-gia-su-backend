from pydantic import BaseModel
from typing import Optional, List
import uuid

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

# Student Profile Schemas
class StudentProfileIn(BaseModel):
    gradeLevel: Optional[str] = None
    learningGoals: Optional[str] = None
    preferredStudyTime: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class StudentProfileOut(BaseModel):
    userId: uuid.UUID
    studentId: uuid.UUID
    gradeLevel: Optional[str] = None
    learningGoals: Optional[str] = None
    preferredStudyTime: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedStudentProfileResponse(BaseModel):
    pagination: PaginationMeta
    data: List[StudentProfileOut]

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
    userId: uuid.UUID
    tutorId: uuid.UUID
    degree: Optional[str] = None
    certificate: Optional[str] = None
    experience: Optional[str] = None
    description: Optional[str] = None
    introVideoUrl: Optional[str] = None

    class Config:
        from_attributes = True

class PaginatedTutorProfileResponse(BaseModel):
    pagination: PaginationMeta
    data: List[TutorProfileOut]
