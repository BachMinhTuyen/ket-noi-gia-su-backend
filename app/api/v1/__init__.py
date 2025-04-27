from fastapi import APIRouter
from . import auth, user, role

router = APIRouter()
router.include_router(auth.router)
router.include_router(role.router)
router.include_router(user.router)
