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
    html = f"""
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
        <div style="text-align: center; padding: 20px 0; background-color: #1e88e5; border-radius: 12px 12px 0 0; color: #ffffff;">
            <h1 style="margin: 0; font-size: 24px; font-weight: 6; font-weight: 500;">
                Kích Hoạt Tài Khoản Của Bạn
            </h1>
        </div>
        <div style="padding: 30px; text-align: center;">
            <p style="font-size: 16px; line-height: 1.6; margin: 0 0 20px;">Chào mừng bạn đến với nền tảng 
                <span style="color: #1e88e5; font-weight: 500;">KẾT NỐI GIA SƯ</span>
                !
            </p>
            <p style="font-size: 16px; line-height: 1.6; margin: 0 0 20px;">
                Vui lòng nhấp vào liên kết bên dưới để kích hoạt tài khoản của bạn và bắt đầu trải nghiệm:
            </p>
            <a href="{verification_link}" 
            style="display: inline-block; padding: 14px 28px; background-color: #1e88e5; color: #ffffff; text-decoration: none; border-radius: 8px; font-size: 16px; font-weight: 500; transition: background-color 0.3s ease; ">
                Kích Hoạt Tài Khoản
            </a>
            <p style="font-size: 16px; line-height: 1.6; margin: 20px 0 0;">
            Nếu bạn không đăng ký tài khoản này, vui lòng bỏ qua email này.
            </p>
        </div>
        <div style="text-align: center; padding: 20px; font-size: 14px; color: #777;">
            <p style="color: #1e88e5; text-decoration: none;">
                Cảm ơn bạn đã chọn chúng tôi! Nếu cần hỗ trợ, hãy liên hệ qua 
                <a href="contact">contact@bachminhtuyen.id.vn</a>.
            </p>
        </div>
    </div>
    """
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
