from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import UserOut, UserUpdate
from app.schemas.response import MessageResponse
from app.crud.user import getAllActiveUsers, getAllNotActiveUsers, getUserById, activateUser, updateUser, deleteUser
from app.core.database import database
import uuid

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/", response_model=List[UserOut])
async def get_all_active_users(db: AsyncSession = Depends(database.get_session)):
    users = await getAllActiveUsers(db)
    return users

@router.get("/not-active", response_model=List[UserOut])
async def get_all_not_active_users(db: AsyncSession = Depends(database.get_session)):
    users = await getAllNotActiveUsers(db)
    return users

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    user = await getUserById(user_id, db)
    return user

@router.post("/activate/{user_id}", response_model=MessageResponse)
async def activate_user(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await activateUser(user_id, db)
    return result

@router.post("/update/{user_id}", response_model=UserOut)
async def update_user(user_id: uuid.UUID, user_update: UserUpdate, db: AsyncSession = Depends(database.get_session)):
    updated_user = await updateUser(user_id, user_update, db)
    return updated_user

@router.delete("/delete/{user_id}", response_model=MessageResponse)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await deleteUser(user_id, db)
    return result