from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.student_request import PaginatedClassResponse, StudentRequestCreate, StudentRequestUpdate
from app.schemas.response import MessageResponse, ResponseWithMessage, MessageResponseWithId
from app.crud import student_request
from app.core.database import database
import uuid

router = APIRouter(prefix="/student-request", tags=["Student Request"])

@router.get('/', response_model=PaginatedClassResponse)
async def get_all_student_request(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await student_request.getAllStudentRequest(db, page, limit)
    return result

@router.get('/get-by-location/{location}', response_model=PaginatedClassResponse)
async def get_all_student_request_by_location(location: str, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await student_request.getAllStudentRequestByLocation(location, db, page, limit)
    return result

@router.get('/get-by-user/{user_id}', response_model=PaginatedClassResponse)
async def get_all_student_request_by_user(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await student_request.getAllStudentRequestByUser(user_id, db, page, limit)
    return result

@router.get('/{request_id}', response_model=ResponseWithMessage)
async def get_student_request_by_id(request_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await student_request.getStudentRequestById(request_id, db)
    return result

@router.post('/create', response_model=MessageResponseWithId)
async def create_student_request(request_data: StudentRequestCreate, db: AsyncSession = Depends(database.get_session)):
    result = await student_request.createStudentRequest(request_data, db)
    return result

@router.put('/update/{request_id}', response_model=ResponseWithMessage)
async def update_student_request(request_id: uuid.UUID, request_data: StudentRequestUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await student_request.updateStudentRequest(request_id, request_data, db)
    return result

@router.delete('/delete/{request_id}', response_model=MessageResponse)
async def delete_student_request(request_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await student_request.deleteStudentRequest(request_id, db)
    return result