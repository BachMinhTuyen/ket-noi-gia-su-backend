from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import database
from app.crud.class_ import getAllClass, getAllClassByStatus, getClassById, createClass, updateClass, deleteClass, findBestClasses
from app.schemas.class_ import ClassCreate, PaginatedClassResponse, ClassUpdate, ClassSearchInput, MatchingClassResponse
from app.schemas.response import ResponseWithMessage, MessageResponse, MessageResponseWithId

router = APIRouter(prefix="/classes", tags=["Class"])

@router.post('/find-best-classes', response_model=MatchingClassResponse)
async def find_best_classes(search_data: ClassSearchInput, db: AsyncSession = Depends(database.get_session)):
    result = await findBestClasses(search_data, db)
    return result

@router.get('/', response_model=PaginatedClassResponse)
async def get_all_class(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllClass(db, page, limit)
    return result

@router.get('/get-by-status/{status_id}', response_model=PaginatedClassResponse)
async def get_all_class_by_status(status_id: uuid.UUID,db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllClassByStatus(status_id, db, page, limit)
    return result

@router.get('/get-by-id/{class_id}', response_model=ResponseWithMessage)
async def get_class_by_id(class_id: uuid.UUID,db: AsyncSession = Depends(database.get_session)):
    result = await getClassById(class_id, db)
    return result

@router.post('/create', response_model=MessageResponseWithId)
async def create_class(class_data: ClassCreate, db: AsyncSession = Depends(database.get_session)):
    result = await createClass(class_data, db)
    return result

@router.put('/update/{class_id}',  response_model=ResponseWithMessage)
async def update_class(class_id: uuid.UUID, class_data: ClassUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await updateClass(class_id, class_data, db)
    return result

@router.delete('/delete/{class_id}', response_model=MessageResponse)
async def delete_class(class_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await deleteClass(class_id, db)
    return result