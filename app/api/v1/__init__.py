from fastapi import APIRouter
from . import (
    auth, 
    user, 
    role, 
    calculate, 
    profile, 
    subject, 
    status, 
    class_, 
    student_request, 
    tutor_application, 
    schedule, 
    class_registration, 
    payment,
    payment_method,
    address,
    zoom,
    statistics,
    complaint,
    complaint_type,
)

router = APIRouter()
router.include_router(calculate.router)
router.include_router(zoom.router)
router.include_router(statistics.router)
router.include_router(auth.router)
router.include_router(role.router)
router.include_router(user.router)
router.include_router(profile.router)
router.include_router(subject.router)
router.include_router(status.router)
router.include_router(class_.router)
router.include_router(class_registration.router)
router.include_router(student_request.router)
router.include_router(tutor_application.router)
router.include_router(schedule.router)
router.include_router(payment.router)
router.include_router(payment_method.router)
router.include_router(address.router)
router.include_router(complaint.router)
router.include_router(complaint_type.router)
