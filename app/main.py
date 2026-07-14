from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1.endpoints import tenants, documents


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MindBot Multi-Tenant RAG Engine",
    description="Enterprise core for context-aware document processing and semantic vector search.",
    version="1.0.0"
)


app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["Tenants"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])



@app.get("/")
def dead_root():
    return {
        "status": "online",
        "service": "MindBot RAG Core",
        "documentation": "/docs" 
    }