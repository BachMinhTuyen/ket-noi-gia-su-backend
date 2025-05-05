from fastapi import APIRouter
from . import auth, user, role, calculate, profile, subject, status, class_, student_request, tutor_application

router = APIRouter()
router.include_router(calculate.router)
router.include_router(auth.router)
router.include_router(role.router)
router.include_router(user.router)
router.include_router(profile.router)
router.include_router(subject.router)
router.include_router(status.router)
router.include_router(class_.router)
router.include_router(student_request.router)
router.include_router(tutor_application.router)
