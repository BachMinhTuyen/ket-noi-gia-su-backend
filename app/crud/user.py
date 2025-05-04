from fastapi import Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import User
from app.schemas.user import UserRegistration, UserUpdate
from app.core.database import database
from app.core.security import decode_access_token, oauth2_scheme, hash_password
from app.crud.profile import createStudentProfile, createTutorProfile
import uuid

async def getCurrentUser(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(database.get_session)):
    user_id = decode_access_token(token)
    result = await db.execute(select(User).filter(User.userId == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def getAllActiveUsers(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    
    total_result = await db.execute(select(func.count())
                                    .select_from(User)
                                    .filter(User.isVerified == True))
    total_items = total_result.scalar()

    result = await db.execute(select(User)
                                .filter(User.isVerified == True)
                                .offset(offset)
                                .limit(limit))
    
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

async def getAllNotActiveUsers(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    
    total_result = await db.execute(select(func.count())
                                    .select_from(User)
                                    .filter(User.isVerified == False))
    total_items = total_result.scalar()

    result = await db.execute(select(User)
                                .filter(User.isVerified == False)
                                .offset(offset)
                                .limit(limit))
    
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

async def getAllUsers(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    
    total_result = await db.execute(select(func.count())
                                    .select_from(User))
    total_items = total_result.scalar()

    result = await db.execute(select(User)
                                .offset(offset)
                                .limit(limit))
    
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

async def getAllUsersByRole(roleId: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    
    total_result = await db.execute(select(func.count())
                                    .select_from(User)
                                    .filter(User.roleId == roleId))
    total_items = total_result.scalar()

    result = await db.execute(select(User)
                                .filter(User.roleId == roleId)
                                .offset(offset)
                                .limit(limit))
    
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

async def getUserById(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(User).filter(User.userId == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def createUser(user_data: UserRegistration, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(User).filter(User.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    result = await db.execute(select(User).filter(User.phoneNumber == user_data.phoneNumber))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        phoneNumber=user_data.phoneNumber,
        password=hash_password(user_data.password),
        fullName=user_data.fullName,
        avatarUrl = "https://res.cloudinary.com/dgl1kzmgc/image/upload/v1745341169/user_default.jpg",
        roleId=user_data.roleId,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "User created successfully"}

async def activateUser(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(User).filter(User.userId == user_id).options(selectinload(User.role)))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role.roleName == "Student":
        new_profile = await createStudentProfile(user_id, db)

    elif user.role.roleName == "Tutor":
        new_profile = await createTutorProfile(user_id, db)
    else:
        raise HTTPException(status_code=400, detail="Invalid user role")
    
    user.isVerified = True
    await db.commit()
    await db.refresh(user)

    if new_profile:
        await db.refresh(new_profile)

    return {"message": "User activated successfully"}

async def updateUser(user_id: uuid.UUID, user_data: UserUpdate, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(User).filter(User.userId == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def deleteUser(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(User).filter(User.userId == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}