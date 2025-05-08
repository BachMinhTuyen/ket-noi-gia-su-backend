from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import database
from app.crud.class_ import getAllClassRegistration, getAllClassRegistrationByStudent, getAllClassRegistrationByClass, getClassRegistrationById, createClassRegistration, deleteClassRegistration
from app.schemas.class_ import ClassRegistrationCreate, PaginatedClassRegistrationResponse, ClassRegistrationOut
from app.schemas.response import ResponseWithMessage, MessageResponse

router = APIRouter(prefix="/class-registration", tags=["Class Registration"])

@router.get('/', response_model=PaginatedClassRegistrationResponse)
async def get_all_class_registration(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllClassRegistration(db, page, limit)
    return result

@router.get('/get-by-class/{class_id}', response_model=PaginatedClassRegistrationResponse)
async def get_all_class_registration_by_class(class_id: uuid.UUID,db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllClassRegistrationByClass(class_id, db, page, limit)
    return result

@router.get('/get-by-student/{student_id}', response_model=PaginatedClassRegistrationResponse)
async def get_all_class_registration_by_class(student_id: uuid.UUID,db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllClassRegistrationByStudent(student_id, db, page, limit)
    return result

@router.get('/get-by-id/{registration_id}', response_model=ResponseWithMessage)
async def get_class_registration_by_id(registration_id: uuid.UUID,db: AsyncSession = Depends(database.get_session)):
    result = await getClassRegistrationById(registration_id, db)
    return result

@router.post('/create', response_model=MessageResponse)
async def create_class(registration_data: ClassRegistrationCreate, db: AsyncSession = Depends(database.get_session)):
    result = await createClassRegistration(registration_data, db)
    return result

@router.delete('/delete/{registration_id}', response_model=MessageResponse)
async def delete_class(registration_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await deleteClassRegistration(registration_id, db)
    return result
