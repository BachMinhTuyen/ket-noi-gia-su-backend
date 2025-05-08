from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from app.core.database import database
from app.models import PaymentStatus, Payment, PaymentMethod, Class, ClassRegistration
from app.schemas.payment import PaymentOrderCreate, PaymentOrderUpdate, PaymentOrderOut, PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodOut
from app.schemas.response import ResponseWithMessage
import uuid



async def getAllPaymentOrders(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Payment))
    total_items = total_result.scalar()

    result = await db.execute(select(Payment).order_by(Payment.registrationId).offset(offset).limit(limit))

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

async def getPaymentOrderById(payment_registration_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):

    res = await db.execute(select(Payment).filter(
        or_(
            Payment.paymentId == payment_registration_id,
            Payment.registrationId == payment_registration_id
        )
    ))
    data = res.scalars().first()
    return data

async def createPaymentOrder(payment_data: PaymentOrderCreate, db: AsyncSession = Depends(database.get_session)):
    exiting_payment = await db.execute(select(Payment).filter(Payment.registrationId == payment_data.registrationId))
    result = exiting_payment.scalars().first()
    if result:
        return { "message": "Payment order already exists" }
    
    # Get payment status
    res = await db.execute(select(PaymentStatus).filter(PaymentStatus.code == "Unpaid"))
    payment_status = res.scalars().first()

    # Get class registration
    registration_res = await db.execute(
        select(ClassRegistration).filter(ClassRegistration.registrationId == payment_data.registrationId)
    )
    registration = registration_res.scalars().first()

    # Get class
    class_res = await db.execute(
        select(Class).filter(Class.classId == registration.classId)
    )
    class_obj = class_res.scalars().first()

    # Calculate total amount
    total_amount = class_obj.tuitionFee * class_obj.sessions

    # Create new payment order
    new_payment_order = Payment(
        **payment_data.dict(),
        amount=total_amount,
        status=payment_status.statusId)
    
    db.add(new_payment_order)
    await db.commit()
    await db.refresh(new_payment_order)
    return { "message": "Payment order created successfully"}

async def updatePaymentOrder(payment_id: uuid.UUID, payment_data: PaymentOrderUpdate, db: AsyncSession = Depends(database.get_session)):
    exiting_payment = await db.execute(select(Payment).filter(Payment.paymentId == payment_id))
    data = exiting_payment.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Payment order not found",
            data=None
        )

    for key, value in payment_data.dict(exclude_unset=True).items():
        setattr(data, key, value)

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return ResponseWithMessage(
        message="Payment order updated successfully",
        data=PaymentOrderOut.model_validate(data)
    )

async def deletePaymentOrder(payment_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    exiting_payment = await db.execute(select(Payment).filter(Payment.paymentId == payment_id))
    data = exiting_payment.scalars().first()
    if not data:
        return { "message": "Payment order not found" }

    await db.delete(data)
    await db.commit()
    return { "message": "Payment order deleted successfully" }



async def getAllPaymentMethods(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(PaymentMethod))
    total_items = total_result.scalar()

    result = await db.execute(select(PaymentMethod).offset(offset).limit(limit))

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

async def getPaymentMethodById(method_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):

    res = await db.execute(select(PaymentMethod).filter(PaymentMethod.methodId == method_id))
    data = res.scalars().first()
    return data

async def createPaymentMethod(method_data: PaymentMethodCreate, db: AsyncSession = Depends(database.get_session)):
    exiting_method = await db.execute(select(PaymentMethod).filter(PaymentMethod.methodName == method_data.methodName))
    result = exiting_method.scalars().first()
    if result:
        return { "message": "Payment method already exists" }
    
    new_method_method = PaymentMethod(**method_data.dict())
    
    db.add(new_method_method)
    await db.commit()
    await db.refresh(new_method_method)
    return { "message": "Payment method created successfully"}

async def activatePaymentMethod(method_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    exiting_method = await db.execute(select(PaymentMethod).filter(PaymentMethod.methodId == method_id))
    data = exiting_method.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Payment method not found",
            data=None
        )

    data.isActive = True

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return { "message": "Payment method has been successfully activated"}

async def updatePaymentMethod(method_id: uuid.UUID, method_data: PaymentMethodUpdate, db: AsyncSession = Depends(database.get_session)):
    exiting_method = await db.execute(select(PaymentMethod).filter(PaymentMethod.methodId == method_id))
    data = exiting_method.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Payment method not found",
            data=None
        )

    for key, value in method_data.dict(exclude_unset=True).items():
        setattr(data, key, value)

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return ResponseWithMessage(
        message="Payment method updated successfully",
        data=PaymentMethodOut.model_validate(data)
    )

async def deletePaymentMethod(method_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    exiting_method = await db.execute(select(PaymentMethod).filter(PaymentMethod.methodId == method_id))
    data = exiting_method.scalars().first()
    if not data:
        return { "message": "Payment method not found" }

    await db.delete(data)
    await db.commit()
    return { "message": "Payment method deleted successfully" }


