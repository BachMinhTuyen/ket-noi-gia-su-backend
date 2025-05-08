from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import database
from app.crud import address
from app.schemas.address import PaginatedAddressResponse, AddressCreate, AddressUpdate
from app.schemas.response import MessageResponse, ResponseWithMessage
import uuid

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.get("/", response_model=PaginatedAddressResponse)
async def get_all_addresses(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await address.getAllAddresses(db, page, limit)
    return result

@router.get("/get-by-id/{user_request_class_id}", response_model=PaginatedAddressResponse)
async def get_all_addresses_by_user_id_or_request_id_or_class_id(user_request_class_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await address.getAllAddressesById(user_request_class_id, db, page, limit)
    return result

@router.post('/create', response_model=MessageResponse)
async def create_address(address_data: AddressCreate, db: AsyncSession = Depends(database.get_session)):
    result = await address.createAddress(address_data, db)
    return result

@router.put('/update/{address_id}', response_model=ResponseWithMessage)
async def update_address(address_id: uuid.UUID, address_data: AddressUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await address.updateAddress(address_id, address_data, db)
    return result

@router.delete('/delete/{address_id}', response_model=MessageResponse)
async def delete_address(address_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await address.deleteAddress(address_id, db)
    return result

