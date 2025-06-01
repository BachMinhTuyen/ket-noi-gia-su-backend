from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import database
from app.models.complaint import Complaint, ComplaintType
from app.schemas.complaint import ComplaintOut, ComplaintCreate, ComplaintUpdate, ComplaintTypeCreate, ComplaintTypeOut, ComplaintTypeUpdate
from app.schemas.response import ResponseWithMessage
import uuid

async def getAllComplaints(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Complaint))
    total_items = total_result.scalar()

    result = await db.execute(select(Complaint)
                            .order_by(Complaint.createdAt.desc())
                            .offset(offset).limit(limit))

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

async def getAllComplaintsByUser(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):

    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Complaint))
    total_items = total_result.scalar()

    result = await db.execute(select(Complaint).filter(Complaint.userId == user_id)
                            .order_by(Complaint.createdAt.desc())
                            .offset(offset).limit(limit))

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

async def getAllComplaintsByStatus(status_name: str, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):

    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Complaint))
    total_items = total_result.scalar()

    result = await db.execute(select(Complaint).filter(Complaint.status == status_name)
                            .order_by(Complaint.createdAt.desc())
                            .offset(offset).limit(limit))

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

async def getComplaintById(complaint_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(Complaint).filter(Complaint.complaintId == complaint_id))
    data = result.scalars().first()
    return data


async def createComplaint(complaint_data: ComplaintCreate, db: AsyncSession = Depends(database.get_session)):
    # Create new complaint
    new_complaint = Complaint(**complaint_data.dict())
    
    db.add(new_complaint)
    await db.commit()
    await db.refresh(new_complaint)
    return { 
        "message": "Complaint created successfully",
        'id':  new_complaint.complaintId
    }

async def updateComplaint(complaint_id: uuid.UUID, complaint_data: ComplaintUpdate, db: AsyncSession = Depends(database.get_session)):
    exiting_complaint = await db.execute(select(Complaint).filter(Complaint.complaintId == complaint_id))
    data = exiting_complaint.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Complaint not found",
            data=None
        )

    for key, value in complaint_data.dict(exclude_unset=True).items():
        setattr(data, key, value)

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return ResponseWithMessage(
        message="Complaint updated successfully",
        data=ComplaintOut.model_validate(data)
    )

async def deleteComplaint(complaint_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    exiting_complaint = await db.execute(select(Complaint).filter(Complaint.complaintId == complaint_id))
    data = exiting_complaint.scalars().first()
    if not data:
        return { "message": "Complaint not found" }

    await db.delete(data)
    await db.commit()
    return { "message": "Complaint deleted successfully" }



async def getAllComplaintTypes(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(ComplaintType))
    total_items = total_result.scalar()

    result = await db.execute(select(ComplaintType)
                            .order_by(ComplaintType.name)
                            .offset(offset).limit(limit))

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

async def getComplaintTypesById(type_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):

    result = await db.execute(select(ComplaintType)
                            .filter(ComplaintType.complaintTypeId == type_id)
                            .order_by(ComplaintType.name))

    data = result.scalars().first()

    return data


async def createComplaintType(complaint_type_data: ComplaintTypeCreate, db: AsyncSession = Depends(database.get_session)):
    # Create new complaint
    new_complaint_type = ComplaintType(**complaint_type_data.dict())
    
    db.add(new_complaint_type)
    await db.commit()
    await db.refresh(new_complaint_type)
    return { 
        "message": "Complaint type created successfully",
        'id':  new_complaint_type.complaintTypeId
    }

async def updateComplaintType(complaint_type_id: uuid.UUID, complaint_type_data: ComplaintTypeUpdate, db: AsyncSession = Depends(database.get_session)):
    exiting_complaint_type = await db.execute(select(ComplaintType).filter(ComplaintType.complaintTypeId == complaint_type_id))
    data = exiting_complaint_type.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Complaint type not found",
            data=None
        )

    for key, value in complaint_type_data.dict(exclude_unset=True).items():
        setattr(data, key, value)

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return ResponseWithMessage(
        message="Complaint type updated successfully",
        data=ComplaintTypeOut.model_validate(data)
    )

async def deleteComplaintType(complaint_type_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    exiting_complaint_type = await db.execute(select(ComplaintType).filter(ComplaintType.complaintTypeId == complaint_type_id))
    data = exiting_complaint_type.scalars().first()
    if not data:
        return { "message": "Complaint type not found" }

    await db.delete(data)
    await db.commit()
    return { "message": "Complaint type deleted successfully" }