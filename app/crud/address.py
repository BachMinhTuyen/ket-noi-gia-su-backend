from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.core.database import database
from app.models import Address
from app.schemas.address import AddressOut, AddressCreate, AddressUpdate
from app.schemas.response import ResponseWithMessage
import uuid

async def getAllAddresses(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Address))
    total_items = total_result.scalar()

    result = await db.execute(select(Address).order_by(Address.province).offset(offset).limit(limit))

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

async def getAllAddressesById(user_request_class_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):

    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(Address))
    total_items = total_result.scalar()

    result = await db.execute(select(Address).filter(
        or_(
            Address.addressId == user_request_class_id,
            Address.userId == user_request_class_id,
            Address.requestId == user_request_class_id,
            Address.classId == user_request_class_id
        )
    ).order_by(Address.province).offset(offset).limit(limit))

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

async def createAddress(address_data: AddressCreate, db: AsyncSession = Depends(database.get_session)):
    # Create new address
    new_address = Address(**address_data.dict())
    
    db.add(new_address)
    await db.commit()
    await db.refresh(new_address)
    return { "message": "Address created successfully"}

async def updateAddress(address_id: uuid.UUID, address_data: AddressUpdate, db: AsyncSession = Depends(database.get_session)):
    exiting_address = await db.execute(select(Address).filter(Address.addressId == address_id))
    data = exiting_address.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Address not found",
            data=None
        )

    for key, value in address_data.dict(exclude_unset=True).items():
        setattr(data, key, value)

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return ResponseWithMessage(
        message="Address updated successfully",
        data=AddressOut.model_validate(data)
    )

async def deleteAddress(address_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    exiting_address = await db.execute(select(Address).filter(Address.addressId == address_id))
    data = exiting_address.scalars().first()
    if not data:
        return { "message": "Address not found" }

    await db.delete(data)
    await db.commit()
    return { "message": "Address deleted successfully" }

