from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from fastapi import HTTPException, Depends
import uuid
from app.core.database import database
from app.models.profile import StudentProfile, TutorProfile
from app.schemas.response import ResponseWithMessage
from app.schemas.profile import StudentProfileIn, StudentProfileOut, TutorProfileIn, TutorProfileOut

async def deleteUserProfile(user_profile_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    # Check student profile
    res_student = await db.execute(
        select(StudentProfile).filter(
            or_(
                StudentProfile.studentId == user_profile_id,
                StudentProfile.userId == user_profile_id,
            )
        )
    )
    student_profile = res_student.scalars().first()

    if student_profile:
        await db.delete(student_profile)
        await db.commit()
        return {"message": "Student profile deleted successfully"}

    # Check tutor profile
    res_tutor = await db.execute(
        select(TutorProfile).filter(
            or_(
                TutorProfile.tutorId == user_profile_id,
                TutorProfile.userId == user_profile_id,
            )
        )
    )
    tutor_profile = res_tutor.scalars().first()

    if tutor_profile:
        await db.delete(tutor_profile)
        await db.commit()
        return {"message": "Tutor profile deleted successfully"}
    
    return { "message": "Profile not found" }


async def getAllStudentProfiles(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(StudentProfile))
    total_items = total_result.scalar()

    result = await db.execute(select(StudentProfile).offset(offset).limit(limit))
    
    data = result.scalars().all()
    total_pages = (total_items + limit - 1) // limit
    
    return {
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        },
        "data": data
    }

async def getStudentProfileByUserId(user_profile_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(StudentProfile).filter(
        or_(
                StudentProfile.studentId == user_profile_id,
                StudentProfile.userId == user_profile_id,
            )
    ))
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


async def getAllTutorProfiles(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(TutorProfile))
    total_items = total_result.scalar()

    result = await db.execute(select(TutorProfile).offset(offset).limit(limit))
    
    data = result.scalars().all()
    total_pages = (total_items + limit - 1) // limit
    
    return {
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        },
        "data": data
    }

async def getTutorProfileByUserId(user_profile_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(TutorProfile).filter(
        or_(
                TutorProfile.tutorId == user_profile_id,
                TutorProfile.userId == user_profile_id,
            )
    ))
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