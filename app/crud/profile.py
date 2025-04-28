from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, Depends
import uuid
from app.core.database import database
from app.models.profile import StudentProfile, TutorProfile
from app.schemas.response import ResponseWithMessage
from app.schemas.profile import StudentProfileIn, StudentProfileOut, TutorProfileIn, TutorProfileOut

async def GetStudentProfileByUserId(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(StudentProfile).filter(StudentProfile.userId == user_id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

async def UpdateStudentProfile(user_id: uuid.UUID, profile_data: StudentProfileIn, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(StudentProfile).filter(StudentProfile.userId == user_id))
    profile = result.scalars().first()
    
    if not profile:
        new_profile = StudentProfile(
            userId=user_id,
            gradeLevel=profile_data.gradeLevel or None,
            learningGoals=profile_data.learningGoals or None,
            preferredStudyTime=profile_data.preferredStudyTime or None,
            description=profile_data.description or None
        )
        db.add(new_profile)
        await db.commit()
        await db.refresh(new_profile)
        return ResponseWithMessage(
            message="User profile updated successfully",
            data=StudentProfileOut.model_validate(profile_data)
        )

    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return ResponseWithMessage(
        message="User profile updated successfully",
        data=StudentProfileOut.model_validate(profile)
    )

async def GetTutorProfileByUserId(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(TutorProfile).filter(TutorProfile.userId == user_id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

async def UpdateTutorProfile(user_id: uuid.UUID, profile_data: TutorProfileIn, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(TutorProfile).filter(TutorProfile.userId == user_id))
    profile = result.scalars().first()
    
    if not profile:
        new_profile = TutorProfile(
            userId=user_id,
            degree=profile_data.degree or None,
            certificate=profile_data.certificate or None,
            experience=profile_data.experience or None,
            description=profile_data.description or None,
            introVideoUrl=profile_data.introVideoUrl or None
        )
        db.add(new_profile)
        await db.commit()
        await db.refresh(new_profile)
        return ResponseWithMessage(
            message="User profile updated successfully",
            data=TutorProfileOut.model_validate(profile_data)
        )

    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return ResponseWithMessage(
        message="User profile updated successfully",
        data=TutorProfileOut.model_validate(profile)
    )