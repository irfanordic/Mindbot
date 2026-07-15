from sqlalchemy.orm import Session
from app.services.embeddings_service import EmbeddingsService
from app.models.document_chunk import DocumentChunk

class RetrievalService():
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingsService()
        
    def retrival_service(self, tenant_id: str,user_query: str, limit: int=4) -> list[str]:
        query_vector = self.embedding_service.get_embeddings(user_query)
        
        results = (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.tenant_id == tenant_id)
            .order_by(DocumentChunk.embedding.cosine_distance(query_vector))
            .limit(limit)
            .all()
        )
        
        
        return [chunk.content for chunk in results]