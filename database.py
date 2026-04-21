from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import Session
from Skills.Base import Base, engine, SessionLocal

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_text = Column(String, nullable=False)
    bot_response = Column(String, nullable=False)
    intent = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

def init_db():
    Base.metadata.create_all(bind=engine)

def save_message(user_text, bot_response, intent):
    db: Session = SessionLocal()
    conversation = Conversation(
        user_text=user_text,
        bot_response=bot_response,
        intent=intent
    )
    db.add(conversation)
    db.commit()
    db.close()

def get_recent_chats(limit=10):
    db: Session = SessionLocal()
    rows = (
        db.query(Conversation)
        .order_by(Conversation.id.desc())
        .limit(limit)
        .all()
    )
    db.close()
    return [
        {
            "user_text": row.user_text,
            "bot_response": row.bot_response,
            "intent": row.intent,
            "timestamp": row.timestamp,
        }
        for row in rows
    ]

def get_total_messages():
    db: Session = SessionLocal()
    total = db.query(Conversation).count()
    db.close()
    return total

def get_intent_stats():
    db: Session = SessionLocal()
    data = (
        db.query(Conversation.intent, func.count(Conversation.intent))
        .group_by(Conversation.intent)
        .order_by(func.count(Conversation.intent).desc())
        .all()
    )
    db.close()
    return [{"intent": intent, "count": count} for intent, count in data]

def clear_db():
    db: Session = SessionLocal()
    db.query(Conversation).delete()
    db.commit()
    db.close()
