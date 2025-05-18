from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.schemas.response import MessageResponse, ResponseWithMessage, MessageResponseWithId
from app.schemas.schedule import PaginatedScheduleResponse, BulkScheduleCreate, ScheduleCreate, ScheduleUpdate
from app.crud import schedule
import uuid

router = APIRouter(prefix="/schedules", tags=["Schedule"])

@router.get("/get-by-class/{class_id}", response_model=PaginatedScheduleResponse)
async def get_all_schedule_by_class(class_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await schedule.getAllScheduleByClass(class_id, db, page, limit)
    return result

@router.get("/get-by-id/{schedule_id}", response_model=ResponseWithMessage)
async def get_all_schedule_by_id(schedule_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await schedule.getScheduleById(schedule_id, db)
    return result

@router.post('/create', response_model=MessageResponseWithId)
async def create_schedule(schedule_data: ScheduleCreate, db: AsyncSession = Depends(database.get_session)):
    result = await schedule.createSchedule(schedule_data, db)
    return result

@router.post('/create-bulk-schedules', response_model=MessageResponse)
async def create_schedule(schedule_data: BulkScheduleCreate, db: AsyncSession = Depends(database.get_session)):
    result = await schedule.createBulkSchedules(schedule_data, db)
    return result

@router.put('/update/{schedule_id}', response_model=ResponseWithMessage)
async def update_schedule(schedule_id: uuid.UUID, schedule_data: ScheduleUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await schedule.updateSchedule(schedule_id, schedule_data, db)
    return result

@router.delete('/delete/{schedule_id}', response_model=MessageResponse)
async def delete_schedule(schedule_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await schedule.deleteSchedule(schedule_id, db)
    return result