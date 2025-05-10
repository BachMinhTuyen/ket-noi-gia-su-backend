from fastapi import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
import uuid

from app.core.config import settings

from app.core.config import settings

class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = 587, # port 465 (SSL/TLS) - port 587 (STARTTLS)
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME= settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_verification_email(
    email: EmailSchema,
    user_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    ) -> JSONResponse:
    verification_link = f"{settings.FRONTEND_URL}/activate/{user_id}"
    html = f"""<p>Click the link to activate your account: {verification_link}</p> """
    message = MessageSchema(
        subject="Activate your account",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    print("Sending email to:", email.email)
    background_tasks.add_task(fm.send_message, message)
    print("Email task scheduled")
    return JSONResponse(status_code=200, content={"message": "Email has been sent"})
