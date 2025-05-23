from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.core.database import database
from app.models import StudentRequest, TutorApplication, Address
from app.schemas.student_request import StudentRequestCreate, StudentRequestOut, StudentRequestUpdate
from app.schemas.response import ResponseWithMessage

async def getAllStudentRequest(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(StudentRequest))
    total_items = total_result.scalar()

    result = await db.execute(select(StudentRequest).offset(offset).limit(limit))

    data = result.scalars().all()
    total_pages = (total_items + limit - 1 ) // limit

    return {
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        },
        "data": data
    }

async def getAllStudentRequestByLocation(location: str, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(StudentRequest).filter(StudentRequest.location == location))
    total_items = total_result.scalar()

    result = await db.execute(select(StudentRequest).filter(StudentRequest.location == location).offset(offset).limit(limit))

    data = result.scalars().all()
    total_pages = (total_items + limit - 1 ) // limit

    return {
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        },
        "data": data
    }

async def getAllStudentRequestByUser(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(StudentRequest).filter(StudentRequest.studentId == user_id))
    total_items = total_result.scalar()

    result = await db.execute(select(StudentRequest).filter(StudentRequest.studentId == user_id).offset(offset).limit(limit))

    data = result.scalars().all()
    total_pages = (total_items + limit - 1 ) // limit

    return {
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        },
        "data": data
    }

async def getAllStudentRequestByStatus(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(StudentRequest).filter(StudentRequest.status == status_id))
    total_items = total_result.scalar()

    result = await db.execute(select(StudentRequest).filter(StudentRequest.status == status_id).offset(offset).limit(limit))

    data = result.scalars().all()
    total_pages = (total_items + limit - 1 ) // limit

    return {
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        },
        "data": data
    }

async def getStudentRequestById(request_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    res = await db.execute(select(StudentRequest).filter(StudentRequest.requestId == request_id))
    data = res.scalars().first()
    if not data:
        return ResponseWithMessage(
            message = "Student request not found",
            data = None
        )
    return ResponseWithMessage(
        message = "Get student request successfully",
        data = StudentRequestOut.model_validate(data)
    )

async def createStudentRequest(request_data: StudentRequestCreate, db: AsyncSession = Depends(database.get_session)):
    new_request = StudentRequest(**request_data.dict())
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    return { 
        'message' : 'Student request created successfully',
        'id':  new_request.requestId
    }

async def updateStudentRequest(request_id: uuid.UUID, request_data: StudentRequestUpdate, db: AsyncSession = Depends(database.get_session)):
    existing_request = await db.execute(select(StudentRequest).filter(StudentRequest.requestId == request_id))
    result = existing_request.scalars().first()
    if not result:
        return ResponseWithMessage(
            message = "Student request not found",
            data = None
        )

    for key, value in request_data.dict(exclude_unset=True).items():
        setattr(result, key, value)

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return ResponseWithMessage(
            message = "Student request updated successfully",
            data = StudentRequestOut.model_validate(result)
        )

async def deleteStudentRequest(request_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_request = await db.execute(select(StudentRequest).filter(StudentRequest.requestId == request_id))
    result = existing_request.scalars().first()
    if not result:
        return { "message" : "Student request not found" }
    
    linked_tutor_application = await db.execute(select(TutorApplication).filter(TutorApplication.requestId == request_id))
    if linked_tutor_application.scalars().first():
        return {"message": "Cannot delete student request because it is linked to TutorApplication"}
    
    linked_address = await db.execute(select(Address).filter(Address.requestId == request_id))
    if linked_address.scalars().first():
        return {"message": "Cannot delete student request because it is linked to Address"}
    
    await db.delete(result)
    await db.commit()
    return { "message": "Student request deleted successfully" }