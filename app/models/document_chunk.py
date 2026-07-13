from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Index, String, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime, timezone


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, nullable=True)
    content     = Column(String, nullable=False)
    embedding   = Column(Vector(1536), nullable=False)
    tenant_id   = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    
Index(
    "idx_document_chunks_embedding",
    DocumentChunk.embedding,
    postgresql_using="hnsw",
    postgresql_ops={"embedding": "vector_cosine_ops"},
)