from google import genai
from app.services.retrieval_service import RetrievalService
from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
import os

class ChatService():
    
    def __init__(self, db: Session):
        
        self.client = genai.Client(api_key= os.getenv("GEMINI_API_KEY"))
        self.retrieval_service = RetrievalService(db=db)
        
    async def answer_question(self, tenant_id: str, question: str):
        
        raw_results = await  self.retrieval_service.retrival_service(
            tenant_id=tenant_id,
            user_query=question
        )    
        
        
        if not raw_results or raw_results[0].distance > 0.55:
            return{
                "answer": "I don't know from the provided documents.",
                "source": []
            }
            
        context_chunks = [item.DocumentChunk.content for item in raw_results]
        context_text = "\n---\n".join(context_chunks)
        
        source_payload = [
            {
                "chunk_index": item.DocumentChunk.chunk_index,
                "chunk_content": item.DocumentChunk.content,
                "distance": round(float(item.distance), 4)
            } for item in raw_results
        ]
        response =   await self.client.aio.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f"Context: {context_text}\n\nQuestion: {question}"
            
        )
        
        
        
        return { 
                "answer": response.text,
                "source": source_payload
                }
        