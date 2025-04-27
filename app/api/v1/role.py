from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models import Role
from app.schemas.user import RoleBase
from app.crud.role import getAllRoles
from app.core.database import database

router = APIRouter(prefix="/roles", tags=["Role"])

@router.get("/", response_model=List[RoleBase])
async def get_all_roles(db: AsyncSession = Depends(database.get_session)):
    result = await getAllRoles(db)
    return result