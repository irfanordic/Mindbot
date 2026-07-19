from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatResponse, ChatRequest
from app.services.chat_service import ChatService
from app.core.security import get_current_tenant
from app.models.tenant import Tenant



router = APIRouter()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def handle_chat(payload: ChatRequest, db: Session=Depends(get_db), current_tenant: Tenant=Depends(get_current_tenant)):
    
    chat_service = ChatService(db=db)
    
    try:
        ai_response  =  await chat_service.answer_question(current_tenant.id, payload.question)
        
        return ChatResponse(answer=ai_response)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={f"AI response failed: {str(e)} "}
        )    