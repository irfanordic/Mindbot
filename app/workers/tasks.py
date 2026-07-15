import asyncio
from app.services.ingestion_service import IngestionService
from app.core.database import sessionLocal
from app.core.celery_app import celery_app



@celery_app.task(name="process_document_task")
def process_document_task(document_id: str):
    db = sessionLocal()
    try:
        
        service = IngestionService(db)
        
        asyncio.run(service.ingest_text(document_id=document_id))
        
    except Exception as e:
        print(f"Error in process_document_task: {e}")
        
    finally:
        db.close()        
        
        
        






