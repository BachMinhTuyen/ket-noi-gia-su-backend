from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from datetime import timedelta
import uuid

from app.core.database import database
from app.models import Class, Schedule, ScheduleStatus
from app.schemas.schedule import BulkScheduleCreate, ScheduleCreate, ScheduleUpdate, ScheduleOut
from app.schemas.response import ResponseWithMessage
from app.deps.time_utils import normalize_time

async def getAllScheduleByClass(class_id: uuid.UUID, db: AsyncSession = Depends(database.get_session), page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count())
                                    .select_from(Schedule)
                                    .filter(Schedule.classId == class_id))
    total_items = total_result.scalar()

    result = await db.execute(select(Schedule).filter(Schedule.classId == class_id).offset(offset).limit(limit))
    
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

async def getScheduleById(schedule_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    data = await db.execute(select(Schedule).filter(Schedule.scheduleId == schedule_id))
    result = data.scalars().first()
    
    if not result:
        return ResponseWithMessage(
            message="Schedule not found",
            data=None
        ) 

    return ResponseWithMessage(
        message="Get schedule successfully",
        data=ScheduleOut.model_validate(result)
    )

async def createSchedule(schedule_data: ScheduleCreate, db: AsyncSession):
    # Get default schedule status
    res = await db.execute(select(ScheduleStatus).filter(ScheduleStatus.code == "Scheduled"))
    shedule_status = res.scalars().first()

    # Get current class
    res = await db.execute(select(Class).filter(Class.classId == schedule_data.classId))
    current_class = res.scalars().first()
    if not current_class:
        return {
            "message": "Class not found",
            'id':  None
        }

    tutor_id = current_class.tutorId
    # Normalize time
    startTime = normalize_time(schedule_data.startTime)
    endTime = normalize_time(schedule_data.endTime)

    # Check conflict schedule of tutor in this day
    conflict_query = select(Schedule).join(Class).filter(
        and_(
            Class.tutorId == tutor_id,
            Schedule.dayStudying == schedule_data.dayStudying,
            or_(
                and_(
                    schedule_data.startTime < Schedule.endTime,
                    schedule_data.endTime > Schedule.startTime
                )
            )
        )
    )
    conflict_query = select(Schedule).join(Class).filter(
        and_(
            Class.tutorId == tutor_id,
            Schedule.dayStudying == schedule_data.dayStudying,
            or_(
                # Case 1: new_start <= existing_end and new_end >= existing_start
                and_(
                    startTime <= Schedule.endTime,
                    endTime >= Schedule.startTime
                ),
                # Case 2: The absolute same time
                and_(
                    startTime == Schedule.endTime,
                    endTime == Schedule.startTime
                )
            )
        )
    )

    conflict_result = await db.execute(conflict_query)
    conflict = conflict_result.scalars().first()

    if conflict:
        return {
            "message": "Tutor already has a schedule at this time",
            'id':  None
        }

    # Create new schedule
    new_schedule = Schedule(
        classId=schedule_data.classId,
        dayStudying=schedule_data.dayStudying,
        startTime=schedule_data.startTime,
        endTime=schedule_data.endTime,
        status=shedule_status.statusId,
        zoomUrl=None,
        zoomMeetingId=None,
        zoomPassword=None
    )
    db.add(new_schedule)
    await db.commit()
    return { 
        "message": "Schedules created successfully",
        'id':  new_schedule.scheduleId
    }

async def createBulkSchedules(schedule_data: BulkScheduleCreate, db: AsyncSession):
    schedules = []

    # Get current class
    res = await db.execute(select(Class).filter(Class.classId == schedule_data.classId))
    current_class = res.scalars().first()
    current_date = current_class.startDate
    if not current_class:
        return {"message": "Class not found"}
    
    tutor_id = current_class.tutorId
    sessions_created = 0

    # Get default schedule status
    res = await db.execute(select(ScheduleStatus).filter(ScheduleStatus.code == "Scheduled"))
    shedule_status = res.scalars().first()

    # Normalize time
    startTime = normalize_time(schedule_data.startTime)
    endTime = normalize_time(schedule_data.endTime)

    while sessions_created < current_class.sessions:
        if current_date.weekday() in schedule_data.weekdays:
            # Check conflict schedule of tutor in this day
            conflict_query = select(Schedule).join(Class).filter(
                and_(
                    Class.tutorId == tutor_id,
                    Schedule.dayStudying == current_date,
                    or_(
                        # Case 1: new_start <= existing_end and new_end >= existing_start
                        and_(
                            startTime <= Schedule.endTime,
                            endTime >= Schedule.startTime
                        ),
                        # Case 2: The absolute same time
                        and_(
                            startTime == Schedule.endTime,
                            endTime == Schedule.startTime
                        )
                    )
                )
            )
            conflict_result = await db.execute(conflict_query)
            conflict = conflict_result.scalars().first()
            if conflict:
                sessions_created += 1
                current_date += timedelta(days=1)
                continue

            # Create new schedule
            new_schedule = Schedule(
                classId=schedule_data.classId,
                dayStudying=current_date,
                startTime=schedule_data.startTime,
                endTime=schedule_data.endTime,
                status=shedule_status.statusId,
                zoomUrl=None,
                zoomMeetingId=None,
                zoomPassword=None
            )
            db.add(new_schedule)
            schedules.append(new_schedule)
            sessions_created += 1
        current_date += timedelta(days=1)

    await db.commit()
    return {"message": "Bulk schedules created successfully"}

async def updateSchedule(schedule_id: uuid.UUID, schedule_data: ScheduleUpdate, db: AsyncSession = Depends(database.get_session)):
    existing_schedule = await db.execute(select(Schedule).filter(Schedule.scheduleId == schedule_id))
    data = existing_schedule.scalars().first()
    if not data:
        return ResponseWithMessage(
            message="Schedule not found",
            data=None
        )

    for key, value in schedule_data.dict(exclude_unset=True).items():
        setattr(data, key, value)

    db.add(data)
    await db.commit()
    await db.refresh(data)
    return ResponseWithMessage(
        message="Schedule updated successfully",
        data=ScheduleOut.model_validate(data)
    )

async def deleteSchedule(schedule_id: uuid.UUID, db: AsyncSession = Depends(database.get_session)):
    existing_schedule = await db.execute(select(Schedule).filter(Schedule.scheduleId == schedule_id))
    data = existing_schedule.scalars().first()
    if not data:
        return { "message": "Schedule not found" }

    await db.delete(data)
    await db.commit()
    return { "message": "Schedule deleted successfully" }