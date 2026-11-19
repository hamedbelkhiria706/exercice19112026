from sqlalchemy.orm import Session
from backend.app.services.db.database import SessionLocal
from backend.app.services.db import models

def add_user(db: Session, email: str, password_hash: str):
    user = models.User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user.id

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_conversation(db: Session, conversation_id: int, user_id: int):
    return (
        db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        ).first()
    )

def get_conversations(db: Session, user_id: int):
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.user_id == user_id)
        .order_by(models.Conversation.updated_at.desc())
        .all()
    )

def delete_conversation(db: Session, conversation_id: int, user_id: int):
    conversation = get_conversation(db, conversation_id, user_id)
    if conversation is None:
        return False
    db.query(models.Message).filter(models.Message.conversation_id == conversation_id).delete()
    db.delete(conversation)
    db.commit()
    return True

def add_message(db: Session, user_id: int, role: str, content: str, conversation_id: int | None = None, tokens_used: int = 0):
    if conversation_id is None:
        conversation = models.Conversation(user_id=user_id, title="New conversation")
        db.add(conversation)
        db.flush()
    else:
        conversation = get_conversation(db, conversation_id, user_id)
        if conversation is None:
            raise LookupError("Conversation not Found")
    message = models.Message(
        conversation_id=conversation.id,
        role=role,
        content=content,
        tokens_used=tokens_used
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message.id, conversation.id

def get_messages(db: Session, conversation_id: int, user_id: int):
    return (
        db.query(models.Message).join(models.Conversation).filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        )
        .order_by(models.Message.id)
        .all()
    )

def create_flashcard_deck(db: Session, user_id: int, title: str):
    deck = models.FlashCardDeck(user_id=user_id, title=title)
    db.add(deck)
    db.commit()
    db.refresh(deck)
    return deck

def get_flashcard_deck(db: Session, deck_id: int, user_id: int | None = None):
    query = db.query(models.FlashCardDeck).filter(models.FlashCardDeck.id == deck_id)
    if user_id is not None:
        query = query.filter(models.FlashCardDeck.user_id == user_id)
    return query.first()

def get_flashcard_decks(db: Session, user_id: int):
    return (
        db.query(models.FlashCardDeck)
        .filter(models.FlashCardDeck.user_id == user_id)
        .order_by(models.FlashCardDeck.created_at.desc())
        .all()
    )

def update_flashcard_deck(db: Session, deck_id: int, title: str, user_id: int | None = None):
    deck = get_flashcard_deck(db, deck_id, user_id)
    if deck is None:
        return None
    deck.title = title
    db.commit()
    db.refresh(deck)
    return deck

def delete_flashcard_deck(db: Session, deck_id: int, user_id: int | None = None):
    deck = get_flashcard_deck(db, deck_id, user_id)
    if deck is None:
        return False
    db.query(models.FlashCard).filter(models.FlashCard.deck_id == deck.id).delete()
    db.delete(deck)
    db.commit()
    return True

def create_flashcard(db: Session, deck_id: int, front: str, back: str):
    flashcard = models.FlashCard(deck_id=deck_id, front=front, back=back)
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

def get_flashcard(db: Session, flashcard_id: int):
    return db.query(models.FlashCard).filter(models.FlashCard.id == flashcard_id).first()

def get_flashcards(db: Session, deck_id: int):
    return (
        db.query(models.FlashCard)
        .filter(models.FlashCard.deck_id == deck_id)
        .order_by(models.FlashCard.id)
        .all()
    )

def update_flashcard(db: Session, flashcard_id: int, front: str | None = None, back: str | None = None):
    flashcard = get_flashcard(db, flashcard_id)
    if flashcard is None:
        return None
    if front is not None:
        flashcard.front = front
    if back is not None:
        flashcard.back = back
    db.commit()
    db.refresh(flashcard)
    return flashcard

def delete_flashcard(db: Session, flashcard_id: int):
    flashcard = get_flashcard(db, flashcard_id)
    if flashcard is None:
        return False
    db.delete(flashcard)
    db.commit()
    return True

def create_deck_with_flashcards(db: Session, user_id: int, title: str, flashcards: list):
    deck = models.FlashCardDeck(user_id=user_id, title=title)
    db.add(deck)
    db.flush()
    for item in flashcards:
        front = getattr(item, "front", None) or (item.get("front") if isinstance(item, dict) else "")
        back = getattr(item, "back", None) or (item.get("back") if isinstance(item, dict) else "")
        card = models.FlashCard(deck_id=deck.id, front=front, back=back)
        db.add(card)
    db.commit()
    db.refresh(deck)
    return deck

def create_quizz(db: Session, user_id: int, topic: str):
    quizz = models.Quizz(user_id=user_id, topic=topic)
    db.add(quizz)
    db.commit()
    db.refresh(quizz)
    return quizz

def get_quizz(db: Session, quizz_id: int, user_id: int | None = None):
    query = db.query(models.Quizz).filter(models.Quizz.id == quizz_id)
    if user_id is not None:
        query = query.filter(models.Quizz.user_id == user_id)
    return query.first()

def get_quizzes(db: Session, user_id: int):
    return (
        db.query(models.Quizz)
        .filter(models.Quizz.user_id == user_id)
        .order_by(models.Quizz.created_at.desc())
        .all()
    )

def update_quizz(db: Session, quizz_id: int, topic: str, user_id: int | None = None):
    quizz = get_quizz(db, quizz_id, user_id)
    if quizz is None:
        return None
    quizz.topic = topic
    db.commit()
    db.refresh(quizz)
    return quizz

def delete_quizz(db: Session, quizz_id: int, user_id: int | None = None):
    quizz = get_quizz(db, quizz_id, user_id)
    if quizz is None:
        return False
    db.query(models.QuizzQuestion).filter(models.QuizzQuestion.quizz_id == quizz.id).delete()
    db.delete(quizz)
    db.commit()
    return True

def create_quizz_question(db: Session, quizz_id: int, question: str, options: list, correct_index: int):
    quizz_question = models.QuizzQuestion(
        quizz_id=quizz_id,
        question=question,
        options=options,
        correct_index=correct_index
    )
    db.add(quizz_question)
    db.commit()
    db.refresh(quizz_question)
    return quizz_question

def get_quizz_question(db: Session, question_id: int):
    return db.query(models.QuizzQuestion).filter(models.QuizzQuestion.id == question_id).first()

def get_quizz_questions(db: Session, quizz_id: int):
    return (
        db.query(models.QuizzQuestion)
        .filter(models.QuizzQuestion.quizz_id == quizz_id)
        .order_by(models.QuizzQuestion.id)
        .all()
    )

def update_quizz_question(
    db: Session,
    question_id: int,
    question: str | None = None,
    options: list | None = None,
    correct_index: int | None = None
):
    quizz_question = get_quizz_question(db, question_id)
    if quizz_question is None:
        return None
    if question is not None:
        quizz_question.question = question
    if options is not None:
        quizz_question.options = options
    if correct_index is not None:
        quizz_question.correct_index = correct_index
    db.commit()
    db.refresh(quizz_question)
    return quizz_question

def delete_quizz_question(db: Session, question_id: int):
    quizz_question = get_quizz_question(db, question_id)
    if quizz_question is None:
        return False
    db.delete(quizz_question)
    db.commit()
    return True

def create_quizz_with_questions(db: Session, user_id: int, topic: str, questions: list):
    quizz = models.Quizz(user_id=user_id, topic=topic)
    db.add(quizz)
    db.flush()
    for item in questions:
        q_text = getattr(item, "question", None) or (item.get("question") if isinstance(item, dict) else "")
        opts = getattr(item, "options", None) or (item.get("options") if isinstance(item, dict) else [])
        c_idx = getattr(item, "correct_index", None)
        if c_idx is None and isinstance(item, dict):
            c_idx = item.get("correct_index")
        if c_idx is None:
            c_val = getattr(item, "correct", None) or (item.get("correct") if isinstance(item, dict) else None)
            if c_val in opts:
                c_idx = opts.index(c_val)
            else:
                c_idx = 0
        qq = models.QuizzQuestion(
            quizz_id=quizz.id,
            question=q_text,
            options=opts,
            correct_index=c_idx
        )
        db.add(qq)
    db.commit()
    db.refresh(quizz)
    return quizz

add_flashcard_deck = create_flashcard_deck
add_flashcard = create_flashcard
get_deck = get_flashcard_deck
get_decks = get_flashcard_decks
update_deck = update_flashcard_deck
delete_deck = delete_flashcard_deck

add_quizz = create_quizz
add_quizz_question = create_quizz_question
get_quiz = get_quizz
get_quizzes_by_user = get_quizzes
delete_quiz = delete_quizz
