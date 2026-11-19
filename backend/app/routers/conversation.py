from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.services.db.database import get_db
from backend.app.services.db import crud

router = APIRouter(prefix="/conversations", tags=["conversations"])
CURRENT_USER = 1

class MessageCreate(BaseModel):
    role: str
    content: str
    tokens_used: int = 0

@router.get("/")
def read_conversations(db: Session = Depends(get_db)):
    return crud.get_conversations(db, CURRENT_USER)

@router.get("/{conversation_id}/messages")
def read_messages(conversation_id: int, db: Session = Depends(get_db)):
    if crud.get_conversation(db, conversation_id, CURRENT_USER) is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return crud.get_messages(db, conversation_id, CURRENT_USER)

@router.post("/{conversation_id}/messages")
def create_message(conversation_id: int, request: MessageCreate, db: Session = Depends(get_db)):
    if crud.get_conversation(db, conversation_id, CURRENT_USER) is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    message_id, conv_id = crud.add_message(
        db, CURRENT_USER, request.role, request.content, conversation_id=conversation_id, tokens_used=request.tokens_used
    )
    return {"message_id": message_id, "conversation_id": conv_id}
