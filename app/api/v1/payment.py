from app.deps.vnpay_utils import VNPAY
from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.core.config import settings
from sqlalchemy import select
from datetime import datetime
from app.crud import payment
from app.models import PaymentStatus, PaymentMethod
from app.schemas.payment import PayOrderData, PaymentOrderOut, PaymentOrderCreate, PaymentOrderUpdate, PaginatedPaymentOrderResponse
from app.schemas.response import MessageResponse, MessageResponseWithId, ResponseWithMessage,MessageResponseWithIdAndRedirect, ResponseWithPaymentMessage
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

@router.post('/create', response_model=MessageResponseWithId)
async def create_payment_order(payment_data: PaymentOrderCreate, db: AsyncSession = Depends(database.get_session)):
    result = await payment.createPaymentOrder(payment_data, db)
    return result

@router.post('/pay-order', response_model=MessageResponseWithIdAndRedirect)
async def pay_order(data: PayOrderData, request: Request, db: AsyncSession = Depends(database.get_session)):
    result = await payment.payOrder(data, request, db)
    return result

@router.get("/vnpay_return", response_model=ResponseWithPaymentMessage)
async def vnpay_return(request: Request, db: AsyncSession = Depends(database.get_session)):
    query_params = dict(request.query_params)

    vnpay = VNPAY(
        tmn_code=settings.VNPAY_TMN_CODE,
        hash_secret=settings.VNPAY_HASH_SECRET_KEY,
        base_url=settings.VNPAY_PAYMENT_URL
    )

    is_valid = vnpay.validate_return_data(query_params)

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid VNPAY signature")

    txn_ref = query_params.get("vnp_TxnRef")
    if not txn_ref:
        raise HTTPException(status_code=400, detail="Missing vnp_TxnRef")

    try:
        payment_id = uuid.UUID(txn_ref)
        # payment_id = txn_ref
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid vnp_TxnRef format")

    # Check VNPAY transaction response code
    vnp_response_code = query_params.get("vnp_ResponseCode")
    if vnp_response_code != "00":
        # Get status "Unpaid"
        status_res = await db.execute(select(PaymentStatus).filter(PaymentStatus.code == "Unpaid"))
        paid_status = status_res.scalars().first()

        # Update payment status
        update_data = PaymentOrderUpdate(
            status=paid_status.statusId if paid_status else None
        )
        await payment.updatePaymentOrder(payment_id=payment_id, payment_data=update_data, db=db)
        return {
            "status": "fail",
            "message": "Payment failed or cancelled by user",
            "vnp_ResponseCode": vnp_response_code
        }

    # Get status "Paid"
    status_res = await db.execute(select(PaymentStatus).filter(PaymentStatus.code == "Paid"))
    paid_status = status_res.scalars().first()

    # Get "VNPAY" method
    method_res = await db.execute(select(PaymentMethod).filter(PaymentMethod.methodName == "VNPAY"))
    vnpay_method = method_res.scalars().first()

    # Update payment
    update_data = PaymentOrderUpdate(
        paidAt=datetime.now(),
        status=paid_status.statusId if paid_status else None,
        methodId=vnpay_method.methodId if vnpay_method else None
    )

    await payment.updatePaymentOrder(payment_id=payment_id, payment_data=update_data, db=db)

    return {
        "status": "success",
        "message": "Payment successful",
        "vnp_ResponseCode": vnp_response_code,
        "payment_id": str(payment_id),
        "vnp_OrderInfo": query_params.get("vnp_OrderInfo"),
        "vnp_Amount": query_params.get("vnp_Amount"),
        "vnp_BankCode": query_params.get("vnp_BankCode"),
        "vnp_PayDate": query_params.get("vnp_PayDate"),
    }

@router.put('/update/{payment_id}', response_model=ResponseWithMessage)
async def update_payment_order(payment_id: uuid.UUID, payment_data: PaymentOrderUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await payment.updatePaymentOrder(payment_id, payment_data, db)
    return result

@router.delete('/delete/{payment_id}', response_model=MessageResponse)
async def delete_payment_order(payment_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await payment.deletePaymentOrder(payment_id, db)
    return result

