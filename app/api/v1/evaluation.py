from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.crud import evaluation
from app.schemas.evaluation import PaginatedEvaluationResponse, EvaluationUpdate, EvaluationCreate, EvaluationOut
from app.schemas.response import MessageResponse, ResponseWithMessage, MessageResponseWithId
import uuid

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

@router.get("/", response_model=PaginatedEvaluationResponse)
async def get_all_evaluation(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await evaluation.getAllEvaluations(db, page, limit)
    return result

@router.get("/get-by-recipient/{user_id}", response_model=PaginatedEvaluationResponse)
async def get_all_recipient_evaluations(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await evaluation.getAllRecipientEvaluations(user_id, db, page, limit)
    return result

@router.get("/get-by-id/{evaluation_id}", response_model=EvaluationOut)
async def get_evaluation_by_evaluation_id(evaluation_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await evaluation.getEvaluationsById(evaluation_id, db)
    return result

@router.post('/create', response_model=MessageResponseWithId)
async def create_evaluation(evaluation_data: EvaluationCreate, db: AsyncSession = Depends(database.get_session)):
    result = await evaluation.createEvaluation(evaluation_data, db)
    return result

@router.put('/update/{evaluation_id}', response_model=ResponseWithMessage)
async def update_evaluation(evaluation_id: uuid.UUID, evaluation_data: EvaluationUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await evaluation.updateEvaluation(evaluation_id, evaluation_data, db)
    return result

@router.delete('/delete/{evaluation_id}', response_model=MessageResponse)
async def delete_evaluation(evaluation_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await evaluation.deleteEvaluation(evaluation_id, db)
    return result

