from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends
import uuid
from app.core.database import database
from app.models.profile import StudentProfile, TutorProfile
from app.schemas.response import ResponseWithMessage
from app.schemas.profile import StudentProfileIn, StudentProfileOut, TutorProfileIn, TutorProfileOut

async def getStudentProfileByUserId(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(StudentProfile).filter(StudentProfile.userId == user_id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

async def createStudentProfile(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    # Check if a student profile already exists
    existing_student_profile = await db.execute(select(StudentProfile).filter(StudentProfile.userId == user_id))
    student_profile = existing_student_profile.scalars().first()
    
    if not student_profile:
        new_profile = StudentProfile(
            userId=user_id,
            gradeLevel=None,
            learningGoals=None,
            preferredStudyTime=None,
            description=None
        )
        db.add(new_profile)
        return new_profile
    return None

async def updateStudentProfile(user_id: uuid.UUID, profile_data: StudentProfileIn, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(StudentProfile).filter(StudentProfile.userId == user_id))
    profile = result.scalars().first()
    
    if not profile:
        return HTTPException(status_code=404, detail="Profile not found")

    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return ResponseWithMessage(
        message="User profile updated successfully",
        data=StudentProfileOut.model_validate(profile)
    )


async def getTutorProfileByUserId(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(TutorProfile).filter(TutorProfile.userId == user_id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

async def createTutorProfile(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_tutor_profile = await db.execute(select(TutorProfile).filter(TutorProfile.userId == user_id))
    tutor_profile = existing_tutor_profile.scalars().first()

    if not tutor_profile:
        new_profile = TutorProfile(
            userId=user_id,
            degree=None,
            certificate=None,
            experience=None,
            description=None,
            introVideoUrl=None,
            isApproved=False
        )
        db.add(new_profile)
        return new_profile
    return None

async def approveTutorProfile(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(TutorProfile).filter(TutorProfile.userId == user_id))
    profile = result.scalars().first()

    profile.isApproved = True
    await db.commit()
    await db.refresh(profile)
    return {"message": "User profile approved successfully"}

async def updateTutorProfile(user_id: uuid.UUID, profile_data: TutorProfileIn, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(TutorProfile).filter(TutorProfile.userId == user_id))
    profile = result.scalars().first()
    
    if not profile:
        return HTTPException(status_code=404, detail="Profile not found")

    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return ResponseWithMessage(
        message="User profile updated successfully",
        data=TutorProfileOut.model_validate(profile)
    )