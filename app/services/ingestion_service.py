from text_processor import TextProcessor
from embeddings_service import EmbeddingsService
from sqlalchemy.orm import session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


from requests import session


class IngestionService:
    def __init__(self,db: session):
        
        self.db = db
        self.processor = TextProcessor()
        self.embeddings_service = EmbeddingsService()
        
        
    def ingest_text(self, document_id: str) -> bool:
        
        
        
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        
        if not doc:
            return False
        
        try:
            raw_text = "This is the internal company policy text..."
            
            
            chunks  = self.processor.split_text(raw_text)
            
            for index,chunks_text in enumerate(chunks):
                
                vector = self.embeddings_service.get_embeddings(chunks_text)
                
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
            
                
            
                
        