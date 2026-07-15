from openai import AsyncOpenAI
from app.services.retrieval_service import RetrievalService
from sqlalchemy.orm import Session
import os

class ChatService():
    
    def __init__(self, db: Session):
        
        self.client = AsyncOpenAI(api_key= os.getenv("OPENAI_API_KEY"))
        self.retrieval_service = RetrievalService(db=db)
        
    async def answer_question(self, tenant_id: str, question: str):
        
        context_chunks  = await  self.retrieval_service.retrival_service(
            tenant_id=tenant_id,
            user_query=question
        )    
        
        context_text = "\n---\n".join(context_chunks)
        
        system_instruction = f"You are a helpful assistant. Use ONLY the following context to answer:\n{context_text}"
        
        response =   await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": question}]
            
        )
        
        return response.choices[0].message.content
        