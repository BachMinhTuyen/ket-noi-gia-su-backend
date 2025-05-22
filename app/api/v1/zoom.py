from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import database
from app.models import Schedule, Class
from app.deps.zoom_utils import create_zoom_meeting
# from app.deps.time_utils import convert_to_iso_utc
from app.schemas.zoom import ZoomMeetingCreate, ZoomMeetingResponse
import uuid

router = APIRouter(prefix="/zoom-api", tags=["Zoom API"])

@router.post("/create-meeting/{schedule_id}", response_model=ZoomMeetingResponse)
async def create_meeting(schedule_id: uuid.UUID, data: ZoomMeetingCreate, db: AsyncSession = Depends(database.get_session)):
    existing_schedule = await db.execute(select(Schedule).filter(Schedule.scheduleId == schedule_id))
    data = existing_schedule.scalars().first()

    existing_class = await db.execute(select(Class).filter(Class.classId == data.classId))
    res = existing_class.scalars().first()

    # iso_time  = convert_to_iso_utc(data.dayStudying, data.startTime)

    meeting = await create_zoom_meeting(
        user_id="me",
        topic=res.className_vi,
        # start_time=iso_time,
        # duration=40
    )

    data.zoomUrl = meeting.get("join_url")
    data.zoomMeetingId = str(meeting.get("id"))
    data.zoomPassword = meeting.get("password")
    data.zoomStartUrl = meeting.get("start_url")

    db.add(data)
    await db.commit()
    await db.refresh(data)

    return {
        "message": "Meeting created successfully",
        "meeting_url": meeting.get("join_url"),
        "start_url": meeting.get("start_url")
    }