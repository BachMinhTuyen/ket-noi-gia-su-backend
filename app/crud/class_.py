from app.crud.payment import createPaymentOrder
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import uuid

from app.core.similarity import compute_cosine_similarity, find_matching_subject
from app.core.distance import haversine
from app.core.database import database
from app.models import Class, Schedule, Address, Evaluation, ClassRegistration, Subject, TutorProfile, User, Role
from app.schemas.class_ import ClassCreate, ClassUpdate, ClassOut, ClassRegistrationCreate, ClassRegistrationOut, ClassSearchInput
from app.schemas.response import ResponseWithMessage

async def findBestClasses(search_data: ClassSearchInput, db: AsyncSession = Depends(database.get_session)):
    keyword = search_data.keyword.lower()
    # Get subjects
    subject_result = await db.execute(select(Subject))
    subjects = subject_result.scalars().all()
    # matched_subject = None

    matched_subject = await find_matching_subject(keyword, subjects)

    if not matched_subject:
        return {"message": "Không tìm thấy môn học phù hợp."}
    
    # Filter classes by subject
    result = await db.execute(
        select(Class).filter(Class.subjectId == matched_subject.subjectId)
    )
    class_list = result.scalars().all()
    
    scores = []

    for c in class_list:
        # Find the coordinates of this class
        class_address_result = await db.execute(
            select(Address).filter(Address.classId == c.classId)
        )
        class_address = class_address_result.scalars().first()
        
        if not class_address or not class_address.latitude or not class_address.longitude:
            continue

        # Find the coordinates of this user
        user_address_result = await db.execute(
            select(Address).filter(Address.userId == search_data.userId)
        )
        user_address = user_address_result.scalars().first()
        
        if not user_address or not user_address.latitude or not user_address.longitude:
            return {"message": "Không tìm thấy địa chỉ người dùng."}

        # Calculate destination
        distance = await haversine(user_address.latitude, user_address.longitude, class_address.latitude, class_address.longitude)

        # 5. Calculate similarity between keyword and description (tutor, class name and subjects)
        tutor_result = await db.execute(
            select(TutorProfile).filter(TutorProfile.userId == c.tutorId)
        )
        tutor = tutor_result.scalars().first()
        description = f"{tutor.description} {c.className_vi} {c.className_en} {c.description}"
        similarity_score = await compute_cosine_similarity(description, keyword)

        # Suppose 10km is far
        # If the destination is more than 10km away, it will switch to measuring suitability. 
        score = similarity_score * 0.7 + (1 - min(distance / 10, 1)) * 0.3 

        scores.append({
            "class_": c,
            "distance": round(distance, 2),
            "similarity": round(similarity_score, 2),
            "score": round(score, 3)
        })

    sorted_result = sorted(scores, key=lambda x: x["score"], reverse=True)

    return {
        "results": [
            {
                "class_": ClassOut.model_validate(item["class_"]),
                "distance_km": item["distance"],
                "similarity": item["similarity"],
                "matching_score": item["score"]
            }
            for item in sorted_result[:search_data.limit]
        ]
    }

async def getAllClass(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(Class))
    total_items = total_result.scalar()

    result = await db.execute(select(Class).offset(offset).limit(limit))
    
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

async def getAllClassByUser(user_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    # Get user
    user_result = await db.execute(select(User).filter(User.userId == user_id))
    user = user_result.scalars().first()
    if not user:
        return {"message": "User not found"}
    
    # Get user role
    role_result = await db.execute(select(Role).filter(Role.roleId == user.roleId))
    role = role_result.scalars().first()
    if not role:
        return {"message": "Role not found"}
    
    if role.roleName == "Tutor":
        total_result = await db.execute(select(func.count())
                                    .select_from(Class)
                                    .filter(Class.tutorId == user_id))
        total_items = total_result.scalar()
        result = await db.execute(select(Class).filter(Class.tutorId == user_id).offset(offset).limit(limit))
        data = result.scalars().all()
    else:
        total_result = await db.execute(select(func.count())
                                    .select_from(Class)
                                    .join(ClassRegistration)
                                    .filter(ClassRegistration.studentId == user_id))
        total_items = total_result.scalar()
        result = await db.execute(select(Class)
                                .join(ClassRegistration)
                                .filter(ClassRegistration.studentId == user_id)
                                .offset(offset).limit(limit))
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

async def getAllClassByStatus(status_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(Class)
                                    .filter(Class.status == status_id))
    total_items = total_result.scalar()

    result = await db.execute(select(Class).filter(Class.status == status_id).offset(offset).limit(limit))
    
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

async def getClassById(class_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    data = await db.execute(select(Class).filter(Class.classId == class_id))
    result = data.scalars().first()
    
    if not result:
        return ResponseWithMessage(
            message="Class not found",
            data=None
        ) 

    return ResponseWithMessage(
        message="Get class information successfully",
        data=ClassOut.model_validate(result)
    )

async def createClass(class_data: ClassCreate, db: AsyncSession = Depends(database.get_session)):
    new_class = Class(**class_data.dict())
    db.add(new_class)
    await db.commit()
    await db.refresh(new_class)
    return { 
        'message' : "Class created successfully",
        'id':  new_class.classId
    }

async def updateClass(class_id: uuid.UUID, class_data: ClassUpdate, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(Class).filter(Class.classId == class_id))
    result = existing_status.scalars().first()
    if not result:
        return ResponseWithMessage(
            message="Class not found",
            data=None
        )

    for key, value in class_data.dict(exclude_unset=True).items():
        setattr(result, key, value)

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return ResponseWithMessage(
        message="Class updated successfully",
        data=ClassOut.model_validate(result)
    )

async def deleteClass(class_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(Class).filter(Class.classId == class_id))
    result = existing_status.scalars().first()
    if not result:
        return { "message": "Class not found" }

    linked_schedules = await db.execute(select(Schedule).filter(Schedule.classId == class_id))
    if linked_schedules.scalars().first():
        return {"message": "Cannot delete class because it is linked to Schedule"}
    
    linked_address = await db.execute(select(Address).filter(Address.classId == class_id))
    if linked_address.scalars().first():
        return {"message": "Cannot delete class because it is linked to Address"}
    
    linked_evaluation = await db.execute(select(Evaluation).filter(Evaluation.classId == class_id))
    if linked_evaluation.scalars().first():
        return {"message": "Cannot delete class because it is linked to Evaluation"}
    
    linked_class_registration = await db.execute(select(ClassRegistration).filter(ClassRegistration.classId == class_id))
    if linked_class_registration.scalars().first():
        return {"message": "Cannot delete class because it is linked to ClassRegistration"}

    await db.delete(result)
    await db.commit()
    return { "message": "Class deleted successfully" }



async def getAllClassRegistration(db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10): 
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(ClassRegistration))
    total_items = total_result.scalar()

    result = await db.execute(select(ClassRegistration).offset(offset).limit(limit))
    
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

async def getAllClassRegistrationByClass(class_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10): 
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(ClassRegistration)
                                    .filter(ClassRegistration.classId == class_id))
    total_items = total_result.scalar()

    result = await db.execute(select(ClassRegistration).filter(ClassRegistration.classId == class_id).offset(offset).limit(limit))
    
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

async def getAllClassRegistrationByStudent(student_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10): 
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(ClassRegistration)
                                    .filter(ClassRegistration.studentId == student_id))
    total_items = total_result.scalar()

    result = await db.execute(select(ClassRegistration).filter(ClassRegistration.studentId == student_id).offset(offset).limit(limit))
    
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

async def getClassRegistrationById(registration_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    data = await db.execute(select(ClassRegistration).filter(ClassRegistration.registrationId == registration_id))
    result = data.scalars().first()
    
    if not result:
        return ResponseWithMessage(
            message="Class registration not found",
            data=None
        ) 

    return ResponseWithMessage(
        message="Get class registration information successfully",
        data=ClassRegistrationOut.model_validate(result)
    )

async def createClassRegistration(registration_data: ClassRegistrationCreate, db: AsyncSession = Depends(database.get_session)):
    existing_registration = await db.execute(select(ClassRegistration).filter(
        and_(
            ClassRegistration.classId == registration_data.classId,
            ClassRegistration.studentId == registration_data.studentId
        )
    ))
    result = existing_registration.scalars().first()

    if result:
        return { 
            'message' : 'Class registration already exists.',
            'id':  None
        }

    new_class_registration = ClassRegistration(**registration_data.dict())
    db.add(new_class_registration)
    await db.commit()
    await db.refresh(new_class_registration)

    # Create invoice
    await createPaymentOrder(new_class_registration.registrationId, db)
    
    return { 
        'message' : 'Class registration created successfully',
        'id':  new_class_registration.registrationId
    }


async def deleteClassRegistration(registration_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_status = await db.execute(select(ClassRegistration).filter(ClassRegistration.registrationId == registration_id))
    result = existing_status.scalars().first()
    if not result:
        return { "message": "Class registration not found" }

    await db.delete(result)
    await db.commit()
    return { "message": "Class registration deleted successfully" }
