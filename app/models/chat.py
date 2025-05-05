from sqlalchemy import Column, ForeignKey, Text, Boolean, String, Integer, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Conversation(Base):
    __tablename__ = 'Conversation'
    conversationId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(20))
    createdAt = Column(TIMESTAMP(timezone=True))

class ConversationParticipant(Base):
    __tablename__ = 'ConversationParticipant'
    participantId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversationId = Column(UUID(as_uuid=True), ForeignKey('Conversation.conversationId'), nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    joinedAt = Column(TIMESTAMP(timezone=True))
    isMuted = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="conversation_participants")

class Message(Base):
    __tablename__ = 'Message'
    messageId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversationId = Column(UUID(as_uuid=True), ForeignKey('Conversation.conversationId'), nullable=False)
    senderId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    content = Column(Text)
    messageType = Column(String(20))
    sentAt = Column(TIMESTAMP(timezone=True))
    isEdited = Column(Boolean, default=False)
    isDeleted = Column(Boolean, default=False)
    
    sender = relationship("User", back_populates="sent_messages")

class MessageFile(Base):
    __tablename__ = 'MessageFile'
    fileId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    messageId = Column(UUID(as_uuid=True), ForeignKey('Message.messageId'), nullable=False)
    fileUrl = Column(Text)
    fileName = Column(String(255))
    fileType = Column(String(50))
    fileSize = Column(Integer)

class MessageStatus(Base):
    __tablename__ = 'MessageStatus'
    statusId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    messageId = Column(UUID(as_uuid=True), ForeignKey('Message.messageId'), nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey('User.userId'), nullable=False)
    isRead = Column(Boolean, default=False)
    readAt = Column(TIMESTAMP(timezone=True))
    
    user = relationship("User", back_populates="message_statuses")
