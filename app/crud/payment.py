from fastapi import Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from app.core.database import database
from app.core.cloudinary_config import *
import cloudinary.uploader
from app.models import PaymentStatus, Payment, PaymentMethod, Class, ClassRegistration
from app.schemas.payment import PaymentOrderCreate, PaymentOrderUpdate, PaymentOrderOut, UpdateActiveStatus, PaymentMethodUpdate, PaymentMethodOut
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
        return { 
            "message": "Payment order already exists",
            'id':  None
        }
    
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
    return { 
        "message": "Payment order created successfully",
        'id':  new_payment_order.paymentId
    }

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

async def createPaymentMethod(
    methodName: str = Form(...),
    description: Optional[str] = Form(None),
    isActive: Optional[bool] = Form(False),
    logo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(database.get_session)
):
    exiting_method = await db.execute(select(PaymentMethod).filter(PaymentMethod.methodName == methodName))
    result = exiting_method.scalars().first()
    if result:
        return { 
            "message": "Payment method already exists",
            'id':  None
        }
    
    # Upload logo to Cloudinary
    logo_url = None
    if logo:
        upload_result = cloudinary.uploader.upload(
            logo.file,
            folder="Connect_With_Tutor/payment_methods",
            public_id=str(uuid.uuid4()),
            overwrite=True,
            resource_type="image"
        )
        logo_url = upload_result.get("secure_url")
        logo_public_id = upload_result.get("public_id")

    new_method = PaymentMethod(
        methodName=methodName,
        description=description,
        isActive=isActive,
        logoUrl=logo_url,
        logoPublicId=logo_public_id,
    )
    
    db.add(new_method)
    await db.commit()
    await db.refresh(new_method)
    return { 
        "message": "Payment method created successfully",
        'id':  new_method.methodId
    }

async def activatePaymentMethod(method_id: uuid.UUID, payload: UpdateActiveStatus, db: AsyncSession = Depends(database.get_session)):
    exiting_method = await db.execute(select(PaymentMethod).filter(PaymentMethod.methodId == method_id))
    data = exiting_method.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Payment method not found",
            data=None
        )

    data.isActive = payload.isActive

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return { "message": "Payment method has been successfully activated"}

async def updatePaymentMethod(
    method_id: uuid.UUID,
    methodName: str = Form(...),
    description: Optional[str] = Form(None),
    isActive: Optional[bool] = Form(False),
    logo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(database.get_session)
):
    exiting_method = await db.execute(
        select(PaymentMethod).filter(PaymentMethod.methodId == method_id)
    )
    data = exiting_method.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Payment method not found",
            data=None
        )
    logo_public_id = data.logoPublicId
    # Delete photos saved on Cloudinary before upload new image
    if data.logoPublicId:
        try:
            cloudinary.uploader.destroy(
                folder="Connect_With_Tutor/payment_methods",
                public_id=logo_public_id,
                resource_type="image"
            )
        except Exception as e:
            print(f"Failed to delete image from Cloudinary: {e}")

    #  upload new image
    logo_url = data.logoUrl
    if logo:
        upload_result = cloudinary.uploader.upload(
            logo.file,
            folder="Connect_With_Tutor/payment_methods",
            public_id=data.logoPublicId,
            overwrite=True,     # Cho phép ghi đè
            invalidate=True,    # xóa cache trên CDN
            resource_type="image",
            filename=logo.filename
        )

        logo_url = upload_result.get("secure_url")
        logo_public_id = upload_result.get("public_id")

    data.methodName = methodName
    data.description = description
    data.isActive = isActive
    data.logoUrl = logo_url
    data.logoPublicId = logo_public_id

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

    # Delete photos saved on Cloudinary before deleting information
    if data.logoPublicId:
        try:
            cloudinary.uploader.destroy(
                folder="Connect_With_Tutor/payment_methods",
                public_id=data.logoPublicId,
                resource_type="image"
            )
        except Exception as e:
            print(f"Failed to delete image from Cloudinary: {e}")

    await db.delete(data)
    await db.commit()
    return { "message": "Payment method deleted successfully" }


