from google import genai
from app.services.retrieval_service import RetrievalService
from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
from app.models.tenant import Tenant, Conversation, Message
from google.genai import types
import os

class ChatService():
    
    def __init__(self, db: Session):
        
        self.client = genai.Client(api_key= os.getenv("GEMINI_API_KEY"))
        self.retrieval_service = RetrievalService(db=db)
        self.db = db
        
    async def answer_question(self, tenant_id: str, conversation_id:str, question: str):
        
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
            
            return{
                "answer": fallback_answer,
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
        
        response =   await self.client.aio.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=content_payload
            
        )
        
        if response.usage_metadata:
            token_used = response.usage_metadata.total_token_count
            tenant = self.db.query(Tenant).filter(Tenant.id==tenant_id).first()
            if tenant:
                tenant.token_used += token_used
                self.db.commit()
            
            
        assist_msg = Message(role="assistant", conversation_id=conversation_id, content=response.text)    
        self.db.add(assist_msg)
        self.db.commit()    
        
        
        
        return { 
                "answer": response.text,
                "source": source_payload
                }
        