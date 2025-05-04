from fastapi import APIRouter
from . import auth, user, role, calculate, profile, subject, status, class_

router = APIRouter()
router.include_router(calculate.router)
router.include_router(auth.router)
router.include_router(role.router)
router.include_router(user.router)
router.include_router(profile.router)
router.include_router(subject.router)
router.include_router(status.router)
router.include_router(class_.router)
