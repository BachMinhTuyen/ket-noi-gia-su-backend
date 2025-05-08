from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.crud import tutor_application
from app.schemas.tutor_application import PaginatedClassResponse, TutorApplicationCreate, TutorApplicationUpdate
from app.schemas.response import MessageResponse, ResponseWithMessage
import uuid

router = APIRouter(prefix="/tutor-application", tags=["Tutor Application"])

@router.get("/", response_model=PaginatedClassResponse)
async def get_all_tutor_applications(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await tutor_application.getAllTutorApplication(db, page, limit)
    return result

@router.get("/get-by-user/{user_id}", response_model=PaginatedClassResponse)
async def get_all_tutor_applications_by_user(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await tutor_application.getAllTutorApplicationByUser(user_id, db, page, limit)
    return result

@router.get("/get-by-request-id/{request_id}", response_model=PaginatedClassResponse)
async def get_all_tutor_applications_by_request_id(request_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await tutor_application.getAllTutorApplicationByRequestId(request_id, db, page, limit)
    return result

@router.get("/get-by-status/{status_id}", response_model=PaginatedClassResponse)
async def get_all_tutor_applications_by_status(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await tutor_application.getAllTutorApplicationByStatus(status_id, db, page, limit)
    return result

@router.post('/create', response_model=MessageResponse)
async def create_tutor_application(application_data: TutorApplicationCreate, db: AsyncSession = Depends(database.get_session)):
    result = await tutor_application.createTutorApplication(application_data, db)
    return result

@router.put('/update/{application_id}', response_model=ResponseWithMessage)
async def update_tutor_application(application_id: uuid.UUID, application_data: TutorApplicationUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await tutor_application.updateTutorApplication(application_id, application_data, db)
    return result

@router.delete('/delete/{application_id}', response_model=MessageResponse)
async def delete_tutor_application(application_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await tutor_application.deleteTutorApplication(application_id, db)
    return result