from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from typing import List
import uuid

class RoleBase(BaseModel):
    roleId: uuid.UUID
    roleName: str

    class Config:
        from_attributesmode = True

# class UserBase(BaseModel):
#     username: str
#     fullName: str
#     birthDate: date
#     phoneNumber: str
#     address: Optional[str]
#     email: EmailStr
#     avatarUrl: Optional[str]
#     averageRating: Optional[float] = 5.0
#     roleId: uuid.UUID
#     isVerified: Optional[bool] = False

class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    phoneNumber: str
    password: str
    fullName: str
    roleId: uuid.UUID

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserUpdate(BaseModel):
    fullName: Optional[str] = None
    birthDate: Optional[date] = None
    phoneNumber: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    avatarUrl: Optional[str] = None

    class Config:
        from_attributesmode = True

class UserOut(BaseModel):
    userId: uuid.UUID
    username: Optional[str] = None
    fullName: Optional[str] = None
    birthDate: Optional[date] = None
    phoneNumber: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    avatarUrl: Optional[str] = None
    averageRating: Optional[float] = None
    roleId: uuid.UUID = None
    isVerified: Optional[bool] = False

    class Config:
        from_attributesmode = True

class PaginationMeta(BaseModel):
    currentPage: int
    totalPages: int
    totalItems: int

class PaginatedUserResponse(BaseModel):
    pagination: PaginationMeta
    data: List[UserOut]

class PaginatedRoleResponse(BaseModel):
    pagination: PaginationMeta
    data: List[RoleBase]

# class UserSocialAccountBase(BaseModel):
#     userId: str
#     provider: Optional[str]
#     providerUserId: Optional[str]
#     email: Optional[EmailStr]

# class UserSocialAccountOut(UserSocialAccountBase):
#     socialAccountId: str
#     linkedAt: Optional[str]

#     class Config:
#         from_attributesmode = True