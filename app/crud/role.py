from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Role
from app.core.database import database

async def getAllRoles(db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(select(Role))
    return result.scalars().all()