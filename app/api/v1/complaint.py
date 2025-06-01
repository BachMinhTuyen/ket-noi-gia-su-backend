from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.crud import complaint
from app.schemas.complaint import PaginatedComplaintResponse, ComplaintUpdate, ComplaintCreate, ComplaintOut
from app.schemas.response import MessageResponse, ResponseWithMessage, MessageResponseWithId
import uuid

router = APIRouter(prefix="/complaint", tags=["Complaint"])

@router.get("/", response_model=PaginatedComplaintResponse)
async def get_all_complaints(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await complaint.getAllComplaints(db, page, limit)
    return result

@router.get("/get-by-status/{status_name}", response_model=PaginatedComplaintResponse)
async def get_all_complaints_by_status_id (status_name: str, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await complaint.getAllComplaintsByStatus(status_name, db, page, limit)
    return result

@router.get("/get-by-user/{user_id}", response_model=PaginatedComplaintResponse)
async def get_all_complaints_by_user_id(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await complaint.getAllComplaintsByUser(user_id, db, page, limit)
    return result

@router.get("/get-by-id/{complaint_id}", response_model=ComplaintOut)
async def get_complainte_by_complaint_id(complaint_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await complaint.getComplaintById(complaint_id, db)
    return result

@router.post('/create', response_model=MessageResponseWithId)
async def create_complaint(complaint_data: ComplaintCreate, db: AsyncSession = Depends(database.get_session)):
    result = await complaint.createComplaint(complaint_data, db)
    return result

@router.put('/update/{complaint_id}', response_model=ResponseWithMessage)
async def update_complaint(complaint_id: uuid.UUID, complaint_data: ComplaintUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await complaint.updateComplaint(complaint_id, complaint_data, db)
    return result

@router.delete('/delete/{complaint_id}', response_model=MessageResponse)
async def delete_complaint(complaint_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await complaint.deleteComplaint(complaint_id, db)
    return result

