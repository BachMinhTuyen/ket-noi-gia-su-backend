from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import database
from app.models import Class, Subject
from app.schemas.statistics import SubjectClassCount

async def getClassCountBySubject(db: AsyncSession = Depends(database.get_session)):
    result = await db.execute(
        select(Class.subjectId, func.count().label("class_count"))
        .group_by(Class.subjectId)
    )
    rows = result.all()

    subject_ids = [row[0] for row in rows]
    subjects_result = await db.execute(
        select(Subject.subjectId, Subject.subjectName_vi)
        .where(Subject.subjectId.in_(subject_ids))
    )
    subjects = subjects_result.all()

    subject_map = {s.subjectId: s.subjectName_vi for s in subjects}

    data = [
        SubjectClassCount(
            subjectId=subjectId,
            subjectName_vi=subject_map.get(subjectId, "Unknown"),
            classCount=class_count
        )
        for subjectId, class_count in rows
    ]

    return data