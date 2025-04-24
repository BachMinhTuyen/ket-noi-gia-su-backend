from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# class RoleBase(BaseModel):
#     roleId: str
#     roleName: Optional[str]

#     class Config:
#         orm_mode = True

class UserBase(BaseModel):
    username: str
    fullName: str
    birthDate: date
    phoneNumber: str
    address: Optional[str]
    email: EmailStr
    avatarUrl: Optional[str]
    averageRating: Optional[float] = 5.0
    roleId: str
    isVerified: Optional[bool] = False

class UserRegistration(UserBase):
    username: str
    email: EmailStr
    phoneNumber: str
    password: str
    fullName: str

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
# class UserOut(UserBase):
#     userId: str
#     username: str
#     email: EmailStr
#     fullName: Optional[str]
    
#     class Config:
#         orm_mode = True

# class UserSocialAccountBase(BaseModel):
#     userId: str
#     provider: Optional[str]
#     providerUserId: Optional[str]
#     email: Optional[EmailStr]

# class UserSocialAccountOut(UserSocialAccountBase):
#     socialAccountId: str
#     linkedAt: Optional[str]

#     class Config:
#         orm_mode = True