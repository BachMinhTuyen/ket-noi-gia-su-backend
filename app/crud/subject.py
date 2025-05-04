from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Subject
from app.schemas.subject import SubjectOut, SubjectCreate, SubjectUpdate
from app.schemas.response import ResponseWithMessage
from app.core.database import database
import uuid

async def getAllSubjects(db: AsyncSession, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Subject))
    total_items = total_result.scalar()

    result = await db.execute(select(Subject).offset(offset).limit(limit))

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

async def createSubject(subject_data: SubjectCreate, db: AsyncSession = Depends(database.get_session)):
    # Check if the subject already exists
    existing_subject = await db.execute(select(Subject).filter(Subject.subjectName_en == subject_data.subjectName_en))
    if existing_subject.scalars().first():
        return {"message": "Subject already exists"}
    
    new_subject = Subject(
        subjectName_vi=subject_data.subjectName_vi,
        subjectName_en=subject_data.subjectName_en,
        description=subject_data.description
    )
    db.add(new_subject)
    await db.commit()
    await db.refresh(new_subject)
    return {"message": "Subject created successfully"}

async def updateSubject(subject_id: uuid.UUID, subject_data: SubjectUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(Subject).filter(Subject.subjectId == subject_id))
    subject = result.scalars().first()
    print('------------------------------------------------------------------------')
    print(subject_data)
    print('------------------------------------------------------------------------')
    if not subject:
        return {"message": "Subject not found"}

    for key, value in subject_data.dict(exclude_unset=True).items():
        setattr(subject, key, value)

    await db.commit()
    await db.refresh(subject)
    return ResponseWithMessage(
        message = "Subject updated successfully", 
        data = SubjectOut.model_validate(subject)
    )

async def deleteSubject(subject_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(Subject).filter(Subject.subjectId == subject_id))
    subject = result.scalars().first()

    if not subject:
        return {"message": "Subject not found"}

    await db.delete(subject)
    await db.commit()
    return {"message": "Subject deleted successfully"}