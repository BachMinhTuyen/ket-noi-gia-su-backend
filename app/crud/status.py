from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import database
from app.models.status import PaymentStatus, ScheduleStatus, StudentRequestStatus, TutorApplicationStatus, ClassStatus
from app.schemas.status import StatusCreate, PaginatedStatusResponse, StatusUpdate, StatusOut
from app.schemas.response import ResponseWithMessage
import uuid



async def getAllPaymentStatus(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(PaymentStatus))
    total_items = total_result.scalar()

    result = await db.execute(select(PaymentStatus).offset(offset).limit(limit))

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

async def createPaymentStatus(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    exiting_status = await db.execute(select(PaymentStatus).filter(PaymentStatus.code == status_data.code))
    result = exiting_status.scalars().first()
    if result:
        return { "message": "Status with this code already exists" }
    
    new_status = PaymentStatus(**status_data.dict())
    db.add(new_status)
    await db.commit()
    await db.refresh(new_status)
    return { "message": "Status created successfully"}

async def updatePaymentStatus(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(PaymentStatus).filter(PaymentStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return ResponseWithMessage(
            message="Status not found",
            data=None
        )

    for key, value in status_data.dict(exclude_unset=True).items():
        setattr(result, key, value)

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return ResponseWithMessage(
        message="Status updated successfully",
        data=StatusOut.model_validate(result)
    )

async def deletePaymentStatus(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(PaymentStatus).filter(PaymentStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return { "message": "Status not found" }

    await db.delete(result)
    await db.commit()
    return { "message": "Status deleted successfully" }



async def getAllScheduleStatus(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(ScheduleStatus))
    total_items = total_result.scalar()

    result = await db.execute(select(ScheduleStatus).offset(offset).limit(limit))

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

async def createScheduleStatus(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    exiting_status = await db.execute(select(ScheduleStatus).filter(ScheduleStatus.code == status_data.code))
    result = exiting_status.scalars().first()
    if result:
        return { "message": "Status with this code already exists" }
    
    new_status = ScheduleStatus(**status_data.dict())
    db.add(new_status)
    await db.commit()
    await db.refresh(new_status)
    return { "message": "Status created successfully"}

async def updateScheduleStatus(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(ScheduleStatus).filter(ScheduleStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return ResponseWithMessage(
            message="Status not found",
            data=None
        )

    for key, value in status_data.dict(exclude_unset=True).items():
        setattr(result, key, value)

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return ResponseWithMessage(
        message="Status updated successfully",
        data=StatusOut.model_validate(result)
    )

async def deleteScheduleStatus(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(ScheduleStatus).filter(ScheduleStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return { "message": "Status not found" }

    await db.delete(result)
    await db.commit()
    return { "message": "Status deleted successfully" }



async def getAllStudentRequestStatus(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(StudentRequestStatus))
    total_items = total_result.scalar()

    result = await db.execute(select(StudentRequestStatus).offset(offset).limit(limit))

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

async def createStudentRequestStatus(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    exiting_status = await db.execute(select(StudentRequestStatus).filter(StudentRequestStatus.code == status_data.code))
    result = exiting_status.scalars().first()
    if result:
        return { "message": "Status with this code already exists" }
    
    new_status = StudentRequestStatus(**status_data.dict())
    db.add(new_status)
    await db.commit()
    await db.refresh(new_status)
    return { "message": "Status created successfully"}

async def updateStudentRequestStatus(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(StudentRequestStatus).filter(StudentRequestStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return ResponseWithMessage(
            message="Status not found",
            data=None
        )

    for key, value in status_data.dict(exclude_unset=True).items():
        setattr(result, key, value)

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return ResponseWithMessage(
        message="Status updated successfully",
        data=StatusOut.model_validate(result)
    )

async def deleteStudentRequestStatus(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(StudentRequestStatus).filter(StudentRequestStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return { "message": "Status not found" }

    await db.delete(result)
    await db.commit()
    return { "message": "Status deleted successfully" }



async def getAllTutorApplicationStatus(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(TutorApplicationStatus))
    total_items = total_result.scalar()

    result = await db.execute(select(TutorApplicationStatus).offset(offset).limit(limit))

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

async def createTutorApplicationStatus(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    exiting_status = await db.execute(select(TutorApplicationStatus).filter(TutorApplicationStatus.code == status_data.code))
    result = exiting_status.scalars().first()
    if result:
        return { "message": "Status with this code already exists" }
    
    new_status = TutorApplicationStatus(**status_data.dict())
    db.add(new_status)
    await db.commit()
    await db.refresh(new_status)
    return { "message": "Status created successfully"}

async def updateTutorApplicationStatus(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(TutorApplicationStatus).filter(TutorApplicationStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return ResponseWithMessage(
            message="Status not found",
            data=None
        )

    for key, value in status_data.dict(exclude_unset=True).items():
        setattr(result, key, value)

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return ResponseWithMessage(
        message="Status updated successfully",
        data=StatusOut.model_validate(result)
    )

async def deleteTutorApplicationStatus(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(TutorApplicationStatus).filter(TutorApplicationStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return { "message": "Status not found" }

    await db.delete(result)
    await db.commit()
    return { "message": "Status deleted successfully" }



async def getAllClassStatus(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(ClassStatus))
    total_items = total_result.scalar()

    result = await db.execute(select(ClassStatus).offset(offset).limit(limit))

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

async def createClassStatus(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    exiting_status = await db.execute(select(ClassStatus).filter(ClassStatus.code == status_data.code))
    result = exiting_status.scalars().first()
    if result:
        return { "message": "Status with this code already exists" }
    
    new_status = ClassStatus(**status_data.dict())
    db.add(new_status)
    await db.commit()
    await db.refresh(new_status)
    return { "message": "Status created successfully"}

async def updateClassStatus(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(ClassStatus).filter(ClassStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return ResponseWithMessage(
            message="Status not found",
            data=None
        )

    for key, value in status_data.dict(exclude_unset=True).items():
        setattr(result, key, value)

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return ResponseWithMessage(
        message="Status updated successfully",
        data=StatusOut.model_validate(result)
    )

async def deleteClassStatus(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(ClassStatus).filter(ClassStatus.statusId == status_id))
    result = existing_status.scalars().first()
    if not result:
        return { "message": "Status not found" }

    await db.delete(result)
    await db.commit()
    return { "message": "Status deleted successfully" }
