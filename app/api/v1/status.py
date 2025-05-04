from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.status import StatusCreate, PaginatedStatusResponse, StatusUpdate
from app.crud import status
from app.core.database import database
from app.schemas.response import MessageResponse, ResponseWithMessage
import uuid

router = APIRouter(prefix="/status", tags=["Status"])

@router.get("/payment", response_model=PaginatedStatusResponse)
async def get_all_payment_status(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await status.getAllPaymentStatus(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No status found")
    return result

@router.post("/payment/create", response_model=MessageResponse)
async def create_payment_status(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    result = await status.createPaymentStatus(status_data, db)
    return result

@router.put("/payment/update/{status_id}", response_model=ResponseWithMessage)
async def update_payment_status(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await status.updatePaymentStatus(status_id, status_data, db)
    return result

@router.delete("/payment/delete/{status_id}", response_model=MessageResponse)
async def delete_payment_status(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await status.deletePaymentStatus(status_id, db)
    return result



@router.get("/schedule", response_model=PaginatedStatusResponse)
async def get_all_schedule_status(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await status.getAllScheduleStatus(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No status found")
    return result

@router.post("/schedule/create", response_model=MessageResponse)
async def create_schedule_status(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    result = await status.createScheduleStatus(status_data, db)
    return result

@router.put("/schedule/update/{status_id}", response_model=ResponseWithMessage)
async def update_schedule_status(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await status.updateScheduleStatus(status_id, status_data, db)
    return result

@router.delete("/schedule/delete/{status_id}", response_model=MessageResponse)
async def delete_schedule_status(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await status.deleteScheduleStatus(status_id, db)
    return result



@router.get("/student-request", response_model=PaginatedStatusResponse)
async def get_all_student_request_status(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await status.getAllStudentRequestStatus(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No status found")
    return result

@router.post("/student-request/create", response_model=MessageResponse)
async def create_student_request_status(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    result = await status.createStudentRequestStatus(status_data, db)
    return result

@router.put("/student-request/update/{status_id}", response_model=ResponseWithMessage)
async def update_student_request_status(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await status.updateStudentRequestStatus(status_id, status_data, db)
    return result

@router.delete("/student-request/delete/{status_id}", response_model=MessageResponse)
async def delete_student_request_status(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await status.deleteStudentRequestStatus(status_id, db)
    return result



@router.get("/tutor-application", response_model=PaginatedStatusResponse)
async def get_all_tutor_application_status(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await status.getAllTutorApplicationStatus(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No status found")
    return result

@router.post("/tutor-application/create", response_model=MessageResponse)
async def create_tutor_application_status(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    result = await status.createTutorApplicationStatus(status_data, db)
    return result

@router.put("/tutor-application/update/{status_id}", response_model=ResponseWithMessage)
async def update_tutor_application_status(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await status.updateTutorApplicationStatus(status_id, status_data, db)
    return result

@router.delete("/tutor-application/delete/{status_id}", response_model=MessageResponse)
async def delete_tutor_application_status(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await status.deleteTutorApplicationStatus(status_id, db)
    return result



@router.get("/class", response_model=PaginatedStatusResponse)
async def get_all_class_status(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await status.getAllClassStatus(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No status found")
    return result

@router.post("/class/create", response_model=MessageResponse)
async def create_class_status(status_data: StatusCreate, db: AsyncSession = Depends(database.get_session)):
    result = await status.createClassStatus(status_data, db)
    return result

@router.put("/class/update/{status_id}", response_model=ResponseWithMessage)
async def update_class_status(status_id: uuid.UUID, status_data: StatusUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await status.updateClassStatus(status_id, status_data, db)
    return result

@router.delete("/class/delete/{status_id}", response_model=MessageResponse)
async def delete_class_status(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await status.deleteClassStatus(status_id, db)
    return result
