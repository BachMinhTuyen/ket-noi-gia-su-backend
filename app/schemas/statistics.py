from pydantic import BaseModel
from typing import List, Optional
import uuid

class SubjectClassCount(BaseModel):
    subjectId: uuid.UUID
    subjectName_vi: str
    classCount: int

class SubjectClassCountList(BaseModel):
    data: Optional[List[SubjectClassCount]] = None