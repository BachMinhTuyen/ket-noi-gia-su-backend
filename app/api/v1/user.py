from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import UserOut, UserUpdate, PaginatedUserResponse
from app.schemas.response import MessageResponse
from app.crud.user import getAllActiveUsers, getAllNotActiveUsers, getAllUsers, getAllUsersByRole, getUserById, activateUser, updateUser, deleteUser
from app.core.database import database
import uuid

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/", response_model=PaginatedUserResponse)
async def get_all_users(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllUsers(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result

@router.get("/actived", response_model=PaginatedUserResponse)
async def get_all_active_users(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllActiveUsers(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result

@router.get("/not-actived", response_model=List[UserOut])
async def get_all_not_active_users(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllNotActiveUsers(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result

@router.get("/get-by-role/{role_id}", response_model=PaginatedUserResponse)
async def get_all_users_by_role(role_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllUsersByRole(role_id, db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    user = await getUserById(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/activate/{user_id}", response_model=MessageResponse)
async def activate_user(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await activateUser(user_id, db)
    return result

@router.put("/update/{user_id}", response_model=UserOut)
async def update_user(user_id: uuid.UUID, user_update: UserUpdate, db: AsyncSession = Depends(database.get_session)):
    updated_user = await updateUser(user_id, user_update, db)
    return updated_user

@router.delete("/delete/{user_id}", response_model=MessageResponse)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await deleteUser(user_id, db)
    return result