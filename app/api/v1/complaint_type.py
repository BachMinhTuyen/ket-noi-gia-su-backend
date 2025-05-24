from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.crud import complaint
from app.schemas.complaint import PaginatedComplaintTypeResponse, ComplaintTypeUpdate, ComplaintTypeCreate, ComplaintTypeOut
from app.schemas.response import MessageResponse, ResponseWithMessage, MessageResponseWithId
import uuid

router = APIRouter(prefix="/complaint-type", tags=["Complaint Type"])

@router.get("/", response_model=PaginatedComplaintTypeResponse)
async def get_all_complaint_types(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await complaint.getAllComplaintTypes(db, page, limit)
    return result

@router.post('/create', response_model=MessageResponseWithId)
async def create_complaint_type(complaint_type_data: ComplaintTypeCreate, db: AsyncSession = Depends(database.get_session)):
    result = await complaint.createComplaintType(complaint_type_data, db)
    return result

@router.put('/update/{complaint_type_id}', response_model=ResponseWithMessage)
async def update_complaint_type(complaint_type_id: uuid.UUID, complaint_type_data: ComplaintTypeUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await complaint.updateComplaintType(complaint_type_id, complaint_type_data, db)
    return result

@router.delete('/delete/{complaint_type_id}', response_model=MessageResponse)
async def delete_complaint_type(complaint_type_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await complaint.deleteComplaintType(complaint_type_id, db)
    return result

