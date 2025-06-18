import datetime
from app.models.class_ import Class
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.core.database import database
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationUpdate, EvaluationCreate, EvaluationOut, PaginatedEvaluationResponse
from app.schemas.response import ResponseWithMessage
import uuid

async def getAllEvaluations(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Evaluation))
    total_items = total_result.scalar()

    result = await db.execute(select(Evaluation)
                            .order_by(Evaluation.evaluationDate.desc())
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
async def getAllRecipientEvaluations (userId: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Evaluation).filter(Evaluation.toUserId == userId))
    total_items = total_result.scalar()

    result = await db.execute(select(Evaluation)
                            .filter(Evaluation.toUserId == userId)
                            .order_by(Evaluation.evaluationDate.desc())
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

async def getEvaluationsById(evaluation_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):

    result = await db.execute(select(Evaluation)
                            .filter(Evaluation.evaluationId == evaluation_id)
                            .order_by(Evaluation.evaluationDate.desc()))

    data = result.scalars().first()

    return data

async def createEvaluation(evaluation_data: EvaluationCreate, db: AsyncSession = Depends(database.get_session)):
    # check if evaluation already exists
    existing_evaluation = await db.execute(
        select(Evaluation).filter(
            and_(
                Evaluation.classId == evaluation_data.classId,
                Evaluation.fromUserId == evaluation_data.fromUserId
            )
        )
    )
    existing_evaluation = existing_evaluation.scalars().first()
    if existing_evaluation:
        return { 
            "message": "Evaluation already exists for this class and user",
            "id": None
        }
    # Get tutorId from classId
    class_query = await db.execute(select(Class).filter(Class.classId == evaluation_data.classId))
    current_class = class_query.scalars().first()

    # Create new evaluation
    new_evaluation = Evaluation(
        **evaluation_data.dict(),
        toUserId=current_class.tutorId
    )
    
    db.add(new_evaluation)
    await db.commit()
    await db.refresh(new_evaluation)
    return { 
        "message": "Evaluation created successfully",
        'id':  new_evaluation.evaluationId
    }

async def updateEvaluation(evaluation_id: uuid.UUID, evaluation_data: EvaluationUpdate, db: AsyncSession = Depends(database.get_session)):
    exiting_evaluation = await db.execute(select(Evaluation).filter(Evaluation.evaluationId == evaluation_id))
    data = exiting_evaluation.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Evaluation not found",
            data=None
        )

    for key, value in evaluation_data.dict(exclude_unset=True).items():
        setattr(data, key, value)

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return ResponseWithMessage(
        message="Evaluation updated successfully",
        data=EvaluationOut.model_validate(data)
    )

async def deleteEvaluation(evaluation_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    exiting_evaluation = await db.execute(select(Evaluation).filter(Evaluation.evaluationId == evaluation_id))
    data = exiting_evaluation.scalars().first()
    if not data:
        return { "message": "Evaluation not found" }

    await db.delete(data)
    await db.commit()
    return { "message": "Evaluation deleted successfully" }