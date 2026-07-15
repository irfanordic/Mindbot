from app.services.text_processor import TextProcessor
from app.services.embeddings_service import EmbeddingsService
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk




class IngestionService:
    def __init__(self,db: Session):
        
        self.db = db
        self.processor = TextProcessor()
        self.embeddings_service = EmbeddingsService()
        
        
    async def ingest_text(self, document_id: str) -> bool:
        
        
        
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        
        if not doc:
            return False
        
        try:
            raw_text = "This is the internal company policy text..."
            
            
            chunks  = self.processor.split_text(raw_text)
            
            for index,chunks_text in enumerate(chunks):
                
                vector = await self.embeddings_service.get_embeddings(chunks_text)
                
                chunk = DocumentChunk(
                    document_id = doc.id,
                    chunk_index = index,
                    page_number = None,
                    content     = chunks_text,
                    embedding = vector,
                    tenant_id = doc.tenant_id
                    
                )
                
                self.db.add(chunk)
                doc.status = "PROCESSED"
                self.db.commit()
                return True
            
        except Exception as e:
            print(f"Error during ingestion: {e}")
            self.db.rollback()
            self.db.commit()
            raise e
            
                
            
                
        