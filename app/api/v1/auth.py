from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
# from contextlib import asynccontextmanager
from sqlalchemy import select
from app.models import User
from app.schemas.user import Token, UserLogin, UserRegistration
from app.core.database import database
from app.core.security import create_access_token, verify_password, decode_access_token, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["Authorization"])

# @router.post("/register")
# async def register(data: UserRegistration, db:Session = Depends(database.get_session)):
    
#     return {
#         "username": data.username, 
#         "email": data.email, 
#         "phoneNumber": data.phoneNumber, 
#         "password": data.password
#     }

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
        domain="localhost",
    )

    return response

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(database.get_session)):
    user_id = decode_access_token(token)
    result = await db.execute(select(User).filter(User.userId == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user