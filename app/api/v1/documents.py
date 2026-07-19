from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.documents import DocumentCreate, DocumentResponse
from app.models.document import Document
from app.models.tenant import Tenant
from app.workers.tasks import process_document_task
from app.services.ingestion_service import IngestionService
from app.core.security import get_current_tenant
import asyncio
import os
import shutil




router = APIRouter()

UPLOAD_DIR = "temporary-uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    current_tenant: Tenant=Depends(get_current_tenant),
    file: UploadFile= File(...),
    db: Session=Depends(get_db) ):
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="only pdf file format are accepted"
        )
        
    upload_path = os.path.join(UPLOAD_DIR, f"{current_tenant.id}_{file.filename}")
    with open(upload_path, "wb") as buffer:    
        shutil.copyfileobj(file.file, buffer)
        
    try:
        
        new_doc=Document(
            filename=file.filename,
            filetype="pdf",
            file_url=upload_path,
            status="PENDING",
            tenant_id=current_tenant.id,
            
        ) 
           
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)   
        
        
        process_document_task.delay(new_doc.id)
    
        return new_doc
        
        
    except Exception as e:
        if os.path.exists(upload_path):
            os.remove(upload_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"cant save document & database error: {str(e)}"
        )    
          
        
          
    
         