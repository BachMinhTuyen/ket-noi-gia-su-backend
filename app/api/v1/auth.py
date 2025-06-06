from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
# from contextlib import asynccontextmanager
from sqlalchemy import select
from app.core.database import database
from app.core.security import create_access_token, verify_password, decode_access_token, oauth2_scheme
from app.core.config import settings
from app.models import User
from app.schemas.user import Token, UserLogin, UserRegistration
from app.schemas.response import MessageResponseWithId
from app.crud.user import createUser
from app.core.email_service import EmailSchema, send_verification_email

router = APIRouter(prefix="/auth", tags=["Authorization"])

@router.post("/register", response_model=MessageResponseWithId)
async def register(data: UserRegistration, background_tasks: BackgroundTasks, db:AsyncSession = Depends(database.get_session)):
    result = await createUser(data, db)
    # Get new_user after new user is saved to database
    user_res = await db.execute(select(User).filter(User.email == data.email))
    new_user = user_res.scalars().first()
    #Send verification email
    await send_verification_email(EmailSchema(email=[data.email]), new_user.userId, background_tasks)
    return result

@router.post("/registration-for-admin-role", response_model=MessageResponseWithId)
async def registration_is_for_admin_role(data: UserRegistration, db:AsyncSession = Depends(database.get_session)):
    result = await createUser(data, db)
    return result

# @asynccontextmanager
# async def login(data: UserLogin, db: AsyncSession = Depends(database.get_session)):
@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(data: UserLogin, db: AsyncSession = Depends(database.get_session)):

    user = None
    if not data.email and not data.phoneNumber:
        raise HTTPException(status_code=400, detail="Email or phone number is required")
    # Admin login with email
    if data.email:
        result = await db.execute(select(User).filter(User.email == data.email))
        user = result.scalars().first()
    # User login with phone number
    elif data.phoneNumber:
        result = await db.execute(select(User).filter(User.phoneNumber == data.phoneNumber))
        user = result.scalars().first()
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify password
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate access token
    access_token = create_access_token(
        data={
            "sub": str(user.userId)
        }
    )
    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "redirect_url": "/dashboard"
    })
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        path="/",
        domain="localhost" if settings.ENVIRONMENT == "development" else None,
        secure=False if settings.ENVIRONMENT == "development" else True,
    )

    return response

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"message": "Successfully logged out"}

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(database.get_session)):
    user_id = decode_access_token(token)
    result = await db.execute(select(User).filter(User.userId == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user