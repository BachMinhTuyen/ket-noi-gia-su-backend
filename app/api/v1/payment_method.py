from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import database
from app.crud import payment
from app.schemas.payment import PaginatedPaymentMethodResponse, UpdateActiveStatus, PaymentMethodOut, PaymentMethodUpdate
from app.schemas.response import MessageResponse, ResponseWithMessage, MessageResponseWithId
import uuid


router = APIRouter(prefix="/payment-methods", tags=["Payment Methods"])


@router.get("/", response_model=PaginatedPaymentMethodResponse)
async def get_all_payment_methods(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await payment.getAllPaymentMethods(db, page, limit)
    return result

@router.get("/get-by-id/{method_id}", response_model=PaymentMethodOut)
async def get_payment_method_by_id(method_id, db: AsyncSession = Depends(database.get_session)):
    result = await payment.getPaymentMethodById(method_id, db)
    return result

@router.post('/create', response_model=MessageResponseWithId)
async def create_payment_method(
    methodName: str = Form(...),
    description: Optional[str] = Form(None),
    isActive: Optional[bool] = Form(False),
    logo: Optional[UploadFile] = File(None), 
    db: AsyncSession = Depends(database.get_session)
):
    result = await payment.createPaymentMethod(methodName, description, isActive, logo, db)
    return result

@router.put('/activate/{method_id}', response_model=ResponseWithMessage)
async def activate_payment_method(method_id: uuid.UUID, payload: UpdateActiveStatus, db: AsyncSession = Depends(database.get_session)):
    result = await payment.activatePaymentMethod(method_id, payload, db)
    return result

@router.put('/update/{method_id}', response_model=ResponseWithMessage)
async def update_payment_method(
    method_id: uuid.UUID,
    methodName: str = Form(...),
    description: Optional[str] = Form(None),
    isActive: Optional[bool] = Form(False),
    logo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(database.get_session)
):
    result = await payment.updatePaymentMethod(method_id, methodName, description, isActive, logo, db)
    return result

@router.delete('/delete/{method_id}', response_model=MessageResponse)
async def delete_payment_method(method_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await payment.deletePaymentMethod(method_id, db)
    return result