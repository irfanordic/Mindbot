from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class DocumentBase(BaseModel):
    filename: str = Field(description="Name of the document")
    filetype: str = Field(description="Type of the document")
    
class DocumentCreate(DocumentBase):
    file_url: str = Field(description="URL of the document file")
    tenant_id: UUID = Field(description="Unique identifier for the tenant associated with the document")
    pass
   
class DocumentResponse(DocumentBase):
    id: UUID = Field(description="Unique identifier for the document")
    created: datetime
    tenant_id: UUID = Field(description="Unique identifier for the tenant associated with the document")
    status: str = Field(description="Status of the document")
    class Config:
        from_attributes = True        
        
    