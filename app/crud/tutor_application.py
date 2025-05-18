from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import Depends
import uuid
from app.core.database import database
from app.models import TutorApplication, StudentRequest, StudentRequestStatus
from app.schemas.response import ResponseWithMessage
from app.schemas.tutor_application import TutorApplicationCreate, TutorApplicationUpdate, TutorApplicationOut


async def getAllTutorApplication(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(TutorApplication))
    total_items = total_result.scalar()

    result = await db.execute(select(TutorApplication).offset(offset).limit(limit))

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

async def getAllTutorApplicationByUser(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(TutorApplication).filter(TutorApplication.tutorId == user_id))
    total_items = total_result.scalar()

    result = await db.execute(select(TutorApplication).filter(TutorApplication.tutorId == user_id).offset(offset).limit(limit))

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

async def getAllTutorApplicationByRequestId(request_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(TutorApplication).filter(TutorApplication.requestId == request_id))
    total_items = total_result.scalar()

    result = await db.execute(select(TutorApplication).filter(TutorApplication.requestId == request_id).offset(offset).limit(limit))

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

async def getAllTutorApplicationByStatus(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(TutorApplication).filter(TutorApplication.status == status_id))
    total_items = total_result.scalar()

    result = await db.execute(select(TutorApplication).filter(TutorApplication.status == status_id).offset(offset).limit(limit))

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

async def createTutorApplication(application_data: TutorApplicationCreate, db: AsyncSession = Depends(database.get_session)):
    # Check student request already exists
    student_request_result = await db.execute(
        select(StudentRequest).filter(StudentRequest.requestId == application_data.requestId)
    )

    student_request = student_request_result.scalars().first()
    
    if not student_request:
        return {
            "message": "Student request not found",
            'id':  None
        }
    
    status_result = await db.execute(
        select(StudentRequestStatus).filter(StudentRequestStatus.code == "Pending")
    )
    pending_status = status_result.scalars().first()

    if not pending_status or student_request.status != pending_status.statusId:
        return {
            "message": "Only requests with 'Pending' status can receive applications",
            'id':  None
        }
    
    # Check if the tutor application already exists
    existing_application = await db.execute(select(TutorApplication).filter(TutorApplication.tutorId == application_data.tutorId))
    if existing_application.scalars().first():
        return {
            "message": "Tutor application already exists",
            'id':  None
        }
    
    new_application = TutorApplication(**application_data.dict())
    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)
    return { 
        "message": "Tutor application created successfully",
        'id':  new_application.applicationId
    }

async def updateTutorApplication(application_id: uuid.UUID, application_data: TutorApplicationUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(TutorApplication).filter(TutorApplication.applicationId == application_id))
    application = result.scalars().first()
    
    if not application:
        return {"message": "Tutor application not found"}

    for key, value in application_data.dict(exclude_unset=True).items():
        setattr(application, key, value)

    await db.commit()
    await db.refresh(application)
    return ResponseWithMessage(
        message = "Tutor application updated successfully", 
        data = TutorApplicationOut.model_validate(application)
    )

async def deleteTutorApplication(application_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(TutorApplication).filter(TutorApplication.applicationId == application_id))
    application = result.scalars().first()

    if not application:
        return {"message": "Tutor application not found"}

    await db.delete(application)
    await db.commit()
    return {"message": "Tutor application deleted successfully"}