from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from .models import ChatResponse, ChatRequest
from backend.app.services.ai import call_llm, AIServiceError
from backend.app.services.errors import ai_error_http
from backend.app.services.db import crud
from backend.app.services.db.database import get_db

router = APIRouter(prefix="/chat", tags=["chat"])
CURRENT_USER = 1

@router.post("/", response_model=ChatResponse)
@router.post("", response_model=ChatResponse, include_in_schema=False)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    clean_msg = request.message.strip()
    if not clean_msg:
        raise HTTPException(status_code=400, detail="Message can not be empty")

    history = []
    if request.conversation_id is not None:
        conversation = crud.get_conversation(db, request.conversation_id, CURRENT_USER)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        history = crud.get_messages(db, request.conversation_id, CURRENT_USER)

    try:
        if history:
            result = call_llm(clean_msg, history=history)
        else:
            result = call_llm(clean_msg)
        _, conversation_id = crud.add_message(
            db, CURRENT_USER, "user", clean_msg, conversation_id=request.conversation_id
        )
        crud.add_message(
            db, CURRENT_USER, "assistant", result["answer"], conversation_id=conversation_id, tokens_used=result["tokens_used"]
        )
    except AIServiceError as error:
        raise ai_error_http(error)

    return ChatResponse(
        answer=result["answer"],
        model=result["model"],
        tokens_used=result["tokens_used"]
    )
