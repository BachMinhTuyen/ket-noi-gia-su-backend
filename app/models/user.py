from sqlalchemy import Column, String, Date, Text, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Role(Base):
    __tablename__ = "Role"
    roleId = Column(UUID, primary_key=True, default=uuid.uuid4)
    roleName = Column(String(20))

    users = relationship("User", back_populates="role", lazy="selectin")

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

    role = relationship("Role", back_populates="users")
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    tutor_profile = relationship("TutorProfile", back_populates="user", uselist=False)
    social_accounts = relationship("UserSocialAccount", back_populates="user")
    student_requests = relationship("StudentRequest", back_populates="student")
    tutor_applications = relationship("TutorApplication", back_populates="tutor")
    created_classes = relationship("Class", back_populates="created_by", foreign_keys='Class.createdBy')
    tutor_classes = relationship("Class", back_populates="tutor", foreign_keys='Class.tutorId')
    class_registrations = relationship("ClassRegistration", back_populates="student")
    sent_evaluations = relationship("Evaluation", back_populates="from_user", foreign_keys='Evaluation.fromUserId')
    received_evaluations = relationship("Evaluation", back_populates="to_user", foreign_keys='Evaluation.toUserId')
    sent_notifications = relationship("Notification", back_populates="from_user", foreign_keys='Notification.fromUserId')
    received_notifications = relationship("Notification", back_populates="to_user", foreign_keys='Notification.toUserId')
    addresses = relationship("Address", back_populates="user")
    conversation_participants = relationship("ConversationParticipant", back_populates="user")
    sent_messages = relationship("Message", back_populates="sender")
    message_statuses = relationship("MessageStatus", back_populates="user")
    complaints = relationship("Complaint", back_populates="user")

class UserSocialAccount(Base):
    __tablename__ = "UserSocialAccount"
    socialAccountId = Column(UUID, primary_key=True, default=uuid.uuid4)
    userId = Column(UUID, ForeignKey("User.userId"), nullable=False)
    provider = Column(String(20))
    providerUserId = Column(String(100))
    email = Column(String(100))
    linkedAt = Column(TIMESTAMP)

    user = relationship("User", back_populates="social_accounts")
