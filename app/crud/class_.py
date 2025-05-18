from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import uuid

from app.core.database import database
from app.models import Class, Schedule, Address, Evaluation, ClassRegistration
from app.schemas.class_ import ClassCreate, ClassUpdate, ClassOut, ClassRegistrationCreate, ClassRegistrationOut
from app.schemas.response import ResponseWithMessage

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
