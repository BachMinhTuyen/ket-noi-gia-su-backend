from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.core.database import database
from app.schemas.profile import StudentProfileIn, StudentProfileOut, TutorProfileIn, TutorProfileOut
from app.schemas.response import ResponseWithMessage
from app.crud.profile import getStudentProfileByUserId, updateStudentProfile, getTutorProfileByUserId, updateTutorProfile

router = APIRouter(prefix="/profiles", tags=["Profile"])

@router.get("/students/{user_id}", response_model=StudentProfileOut)
async def get_student_profile_by_user_id(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await getStudentProfileByUserId(user_id, db)
    return result

@router.put("/students/update/{user_id}", response_model=ResponseWithMessage)
async def update_student_profile(user_id: uuid.UUID, profile_data: StudentProfileIn, db: AsyncSession = Depends(database.get_session)):
    result = await updateStudentProfile(user_id, profile_data, db)
    return result

@router.get("/tutors/{user_id}", response_model=TutorProfileOut)
async def get_tutor_profile_by_user_id(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await getTutorProfileByUserId(user_id, db)
    return result

@router.put("/tutors/update/{user_id}", response_model=ResponseWithMessage)
async def update_tutor_profile(user_id: uuid.UUID, profile_data: TutorProfileIn, db: AsyncSession = Depends(database.get_session)):
    result = await updateTutorProfile(user_id, profile_data, db)
    return result