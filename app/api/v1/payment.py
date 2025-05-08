from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.crud import payment
from app.schemas.payment import PaymentOrderOut, PaymentOrderCreate, PaymentOrderUpdate, PaginatedPaymentOrderResponse
from app.schemas.response import MessageResponse, ResponseWithMessage
import uuid

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/", response_model=PaginatedPaymentOrderResponse)
async def get_all_payment_orders(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await payment.getAllPaymentOrders(db, page, limit)
    return result

@router.get("/get-by-id/{payment_registration_id}", response_model=PaymentOrderOut)
async def get_payment_order_by_payment_id_or_registation_id(payment_registration_id, db: AsyncSession = Depends(database.get_session)):
    result = await payment.getPaymentOrderById(payment_registration_id, db)
    return result

@router.post('/create', response_model=MessageResponse)
async def create_payment_order(payment_data: PaymentOrderCreate, db: AsyncSession = Depends(database.get_session)):
    result = await payment.createPaymentOrder(payment_data, db)
    return result

@router.put('/update/{payment_id}', response_model=ResponseWithMessage)
async def update_payment_order(payment_id: uuid.UUID, payment_data: PaymentOrderUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await payment.updatePaymentOrder(payment_id, payment_data, db)
    return result

@router.delete('/delete/{payment_id}', response_model=MessageResponse)
async def delete_payment_order(payment_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await payment.deletePaymentOrder(payment_id, db)
    return result

