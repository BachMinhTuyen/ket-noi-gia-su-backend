from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.crud.subject import getAllSubjects, createSubject, updateSubject, deleteSubject
from app.schemas.subject import SubjectCreate, PaginatedSubjectResponse, SubjectUpdate
from app.schemas.response import MessageResponse, ResponseWithMessage
import uuid

router = APIRouter(prefix="/subject", tags=["Subject"])

@router.get("/", response_model=PaginatedSubjectResponse)
async def get_all_subjects(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllSubjects(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No subjects found")
    return result

@router.post('/create', response_model=MessageResponse)
async def create_subject(subject_data: SubjectCreate, db: AsyncSession = Depends(database.get_session)):
    result = await createSubject(subject_data, db)
    return result

@router.put('/update/{subject_id}', response_model=ResponseWithMessage)
async def update_subject(subject_id: uuid.UUID, subject_data: SubjectUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await updateSubject(subject_id, subject_data, db)
    return result

@router.delete('/delete/{subject_id}', response_model=MessageResponse)
async def delete_subject(subject_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await deleteSubject(subject_id, db)
    return result