from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.core.database import database
from app.schemas.profile import StudentProfileIn, StudentProfileOut, TutorProfileIn, TutorProfileOut
from app.schemas.response import ResponseWithMessage, MessageResponse
from app.crud import profile

router = APIRouter(prefix="/profiles", tags=["Profile"])

@router.get("/students/{user_id}", response_model=StudentProfileOut)
async def get_student_profile_by_user_id(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await profile.getStudentProfileByUserId(user_id, db)
    return result

@router.put("/students/update/{user_id}", response_model=ResponseWithMessage)
async def update_student_profile(user_id: uuid.UUID, profile_data: StudentProfileIn, db: AsyncSession = Depends(database.get_session)):
    result = await profile.updateStudentProfile(user_id, profile_data, db)
    return result

@router.get("/tutors/{user_id}", response_model=TutorProfileOut)
async def get_tutor_profile_by_user_id(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await profile.getTutorProfileByUserId(user_id, db)
    return result

@router.post("/tutors/approve/{user_id}", response_model=MessageResponse)
async def approve_tutor_profile(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await profile.approveTutorProfile(user_id, db)
    return result

@router.put("/tutors/update/{user_id}", response_model=ResponseWithMessage)
async def update_tutor_profile(user_id: uuid.UUID, profile_data: TutorProfileIn, db: AsyncSession = Depends(database.get_session)):
    result = await profile.updateTutorProfile(user_id, profile_data, db)
    return result

@router.delete('/delete/{user_profile_id}', response_model=MessageResponse)
async def delete_user_profile(user_profile_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await profile.deleteUserProfile(user_profile_id, db)
    return result