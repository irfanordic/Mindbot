from google import genai
from app.services.retrieval_service import RetrievalService
from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
from app.models.tenant import Tenant, Conversation, Message
from google.genai import types
import os
import json

class ChatService():
    
    def __init__(self, db: Session):
        
        self.client = genai.Client(api_key= os.getenv("GEMINI_API_KEY"))
        self.retrieval_service = RetrievalService(db=db)
        self.db = db
        
    async def answer_question_stream(self, tenant_id: str, conversation_id:str, question: str):
        
        if not conversation_id:
            db_convo = Conversation(tenant_id=tenant_id)
            self.db.add(db_convo)
            self.db.commit()
            self.db.refresh(db_convo)
            conversation_id = db_convo.id
            history_messages = []
        else:
            
            recent_messages = (self.db.query(Message)
                              .filter(Message.conversation_id == conversation_id)
                              .order_by(Message.created_at.desc())
                              .limit(5)
                              .all()
            )    
            
            history_messages = list(reversed(recent_messages))
        
        
        
        
        
        
        raw_results = await  self.retrieval_service.retrival_service(
            tenant_id=tenant_id,
            user_query=question
        )    
        
        
        user_msg = Message(
            role = "user",
            content = question,
            conversation_id = conversation_id
        )
        
        self.db.add(user_msg)
        self.db.commit()
        self.db.refresh()
        
        
        
        if not raw_results or raw_results[0].distance > 0.55:
            fallback_answer = "I don't know from the provided documents."
            assist_msg = Message(role= "assistant", conversation_id = conversation_id, content=fallback_answer)
            self.db.add(assist_msg)
            self.db.commit()
            
            yield  f"data: {json.dumps({'answer': fallback_answer, 'source': []})}\n\n"
            return  
            
            
            
        context_chunks = [item.DocumentChunk.content for item in raw_results]
        context_text = "\n---\n".join(context_chunks)
        
        source_payload = [
            {
                "chunk_index": item.DocumentChunk.chunk_index,
                "chunk_content": item.DocumentChunk.content,
                "distance": round(float(item.distance), 4)
            } for item in raw_results
        ]
        
        
        yield f"data: {json.dumps({'source': source_payload})}\n\n"
        
        content_payload = []
        for msg in history_messages:
            sdk_role = "model" if msg.role == "assistant" else 'user'
            content_payload.append(
                types.Content(role=sdk_role, parts=[types.Part.from_text(text=msg.content)])
            )
        
        
        current_prompt = f"Context from system documents:\n{context_text}\n\nQuestion: {question}\n\nAnswer using only the provided context context."
        content_payload.append(
            types.Content(role="user", parts=[types.Part.from_text(text=current_prompt)])
        )
        
        response_stream =   await self.client.aio.models.generate_content_stream(
            model="gemini-3.1-flash-lite",
            contents=content_payload
            
        )
        
        full_response_text = ""
        
        
        
        
        async for chunk in response_stream:
            last_chunk = chunk
            if chunk.text:
                full_response_text += chunk.text
                yield f"data: {chunk.text}\n\n"
                
               
        if last_chunk and  last_chunk.usage_metadata:
            token_used = last_chunk.usage_metadata.total_token_count
            tenant = self.db.query(Tenant).filter(Tenant.id==tenant_id).first()
            if tenant:
                tenant.token_used += token_used
                self.db.commit()     
        
        
        
        
        
        
            
            
        assist_msg = Message(role="assistant", conversation_id=conversation_id, content=full_response_text)    
        self.db.add(assist_msg)
        self.db.commit()    
        
        
        
        yield "data: [DONE]\n\n"
        