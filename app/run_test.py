import asyncio
from app.core.database import get_db, sessionLocal
from app.services.ingestion_service import IngestionService

# Force SQLAlchemy to recognize the relationship tables
from app.models.tenant import Tenant  # Make sure this matches your tenant model file path!
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

async def main():
    # 1. Open a temporary direct database session
    db = sessionLocal()
    try:
        # 2. Instantiate your service
        ingestion_service = IngestionService(db)
        
        # 3. Target the Document ID you want to process
        # TODO: Replace the string below with a real UUID from your DBeaver 'documents' table!
        target_document_id = "6d1bdfbd-098a-48a3-9f80-da7f2bf1efc3"
        
        print(f"Starting manual test ingestion for document: {target_document_id}...")
        
        # 4. Fire the coroutine function directly
        success = await ingestion_service.ingest_text(document_id=target_document_id)
        
        if success:
            print("🎉 Success! Check your DBeaver document_chunks table now.")
        else:
            print("❌ Ingestion returned False. Make sure that document ID exists in your DB.")
            
    except Exception as e:
        print(f"💥 Script crashed with error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())