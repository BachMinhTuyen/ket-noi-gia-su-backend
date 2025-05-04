from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import RoleBase, PaginatedRoleResponse
from app.crud.role import getAllRoles, getRoleById
from app.core.database import database
import uuid

router = APIRouter(prefix="/roles", tags=["Role"])

@router.get("/", response_model=PaginatedRoleResponse)
async def get_all_roles(db: AsyncSession = Depends(database.get_session), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    result = await getAllRoles(db, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No roles found")
    return result

@router.get("/{role_id}", response_model=RoleBase)
async def get_role_by_id(role_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    result = await getRoleById(role_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Role not found")
    return result