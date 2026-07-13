from app.core.database import Base 
from sqlalchemy import Column, String, DateTime, Integer, Boolean
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
    
    
    
    
    