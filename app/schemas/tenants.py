from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class TenantBase(BaseModel):
    name: str = Field(description = "Name of the tenant")
    email: EmailStr = Field(description = "Email address of the tenant")
    
    
    
class TenantCreate(TenantBase):
    pass


class TenantResponse(TenantBase):
    id: UUID = Field(description = "Unique identifier for the tenant")
    created: datetime
    api_key: str = Field(description = "API key for the tenant")
    is_active: bool = Field(description = "Indicates if the tenant is active")
    class Config:
        from_attributes = True
    
            