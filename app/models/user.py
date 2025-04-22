from sqlalchemy import Column, String, Date, Text, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class Role(Base):
    __tablename__ = "Role"
    roleId = Column(UUID, primary_key=True, default=uuid.uuid4)
    roleName = Column(String(20))

class User(Base):
    __tablename__ = "User"
    userId = Column(UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    fullName = Column(String(50), nullable=False)
    birthDate = Column(Date)
    phoneNumber = Column(String(20))
    address = Column(String(50))
    email = Column(String(50))
    avatarUrl = Column(Text)
    averageRating = Column(DECIMAL(3, 2), default=5)
    roleId = Column(UUID, ForeignKey("Role.roleId"), nullable=False)
    isVerified = Column(Boolean, default=False)

class UserSocialAccount(Base):
    __tablename__ = "UserSocialAccount"
    socialAccountId = Column(UUID, primary_key=True, default=uuid.uuid4)
    userId = Column(UUID, ForeignKey("User.userId"), nullable=False)
    provider = Column(String(20))
    providerUserId = Column(String(100))
    email = Column(String(100))
    linkedAt = Column(TIMESTAMP)
