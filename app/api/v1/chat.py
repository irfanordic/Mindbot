from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatResponse, ChatRequest, MessageFeedbackRequest
from app.services.chat_service import ChatService
from app.core.security import get_current_tenant
from app.models.tenant import Tenant, Message
from fastapi.responses import StreamingResponse


router = APIRouter()


@router.post("/",  status_code=status.HTTP_200_OK)
async def handle_chat(payload: ChatRequest, db: Session=Depends(get_db), current_tenant: Tenant=Depends(get_current_tenant)):
    
    chat_service = ChatService(db=db)
    
    return StreamingResponse(
        chat_service.answer_question_stream(
            current_tenant.id,
            payload.conversation_id,
            payload.question
        ),
        media_type="text/event-stream"
    )
    
   
        
@router.post("/feedback", status_code=status.HTTP_200_OK)
async def submit_feedback(
    payload: MessageFeedbackRequest,
    db: Session = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    
    message = db.query(Message).filter(Message.id == payload.message_id).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found."
        )
        
    
    
    message.feedback = payload.rating
    db.commit()
    
    return {"status": "success", "message": "Feedback submitted successfully."}        