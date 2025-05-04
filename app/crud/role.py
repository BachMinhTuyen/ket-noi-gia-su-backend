from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from app.models import Role
from app.core.database import database
import uuid

async def getAllRoles(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(Role))
    total_items = total_result.scalar()

    result = await db.execute(select(Role).offset(offset).limit(limit))
    
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

async def getRoleById(role_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(Role).filter(Role.roleId == role_id))
    return result.scalars().first()