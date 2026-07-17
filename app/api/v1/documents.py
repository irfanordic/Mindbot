from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.documents import DocumentCreate, DocumentResponse
from app.models.document import Document
from app.workers.tasks import process_document_task
from app.services.ingestion_service import IngestionService
import asyncio


router = APIRouter()

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_200_OK)
def upload_document(doc_in: DocumentCreate, db: Session = Depends(get_db)):
    
    new_doc=Document(
        filename= doc_in.filename,
        filetype=doc_in.filetype,
        file_url=doc_in.file_url,
        status="PENDING",
        tenant_id=doc_in.tenant_id
    )
    
    
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    process_document_task.delay(new_doc.id)
    
    return new_doc
    