from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import sessionLocal, get_db
from app.schemas.chat import ChatResponse, ChatRequest
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def handle_chat(payload: ChatRequest, db: Session=Depends(get_db)):
    
    chat_service = ChatService(db=db)
    
    try:
        ai_response  =  await chat_service.answer_question(payload.tenant_id, payload.question)
        
        return ChatResponse(answer=ai_response)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={f"AI response failed: {str(e)} "}
        )    