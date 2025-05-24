from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import database
from app.schemas.statistics import SubjectClassCountList
from app.crud.statistics import getClassCountBySubject

router = APIRouter(prefix="/statistics", tags=["Statistics"] )

@router.get("/classes-by-subject", response_model=SubjectClassCountList)
async def get_class_count_by_subject(db: AsyncSession = Depends(database.get_session)):
    data = await getClassCountBySubject(db);
    return {"data": data}
