from app.core.database import Base 
from sqlalchemy import Column, String, DateTime, Integer, Boolean,  ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone


class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    api_key = Column(String, nullable=False, unique=True)
    token_used = Column(Integer, default=0, nullable=False)
    
    
class Conversation(Base):
    __tablename__= "conversations"
    
    
    id = Column(UUID(as_uuid=True), primary_key=true, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
          
class Message(Base):
    
    
    __tablename__="messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    feedback = Column(String, nullable=True)
    Conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
        
        
    )
        

    
    
    
    