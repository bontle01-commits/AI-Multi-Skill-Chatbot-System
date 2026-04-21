from Skills.Base import Skill, SessionLocal
from sqlalchemy import Column, Integer, String
from Skills.Base import Base

class MentalHealthEntry(Base):
    __tablename__ = "mental_health"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, nullable=False)
    response = Column(String, nullable=False)


class MentalHealthSupport(Skill):
    def can_handle(self, user_input, context):
        # INTENT-based routing (from router)
        return context.get("intent") == "mental"

    def handle(self, user_input, context):
        msg = user_input.lower().strip()
        db = SessionLocal()

        if context.get_state("mental_mode") is None:
            context.set_state("mental_mode", "chat")
            db.close()
            return (
                "💙 Mental Health Support Activated\n\n"
                "I'm here to listen and support you.\n\n"
                "You can tell me how you're feeling:\n"
                "- stressed 😔\n"
                "- anxious 😟\n"
                "- sad 💔\n"
                "- overwhelmed 🌧️\n\n"
                "Or just talk to me. I'm here for you."
            )

        entry = db.query(MentalHealthEntry).filter(MentalHealthEntry.keyword.in_(msg.split())).first()
        db.close()

        if entry:
            return entry.response

        if "exit" in msg or "stop" in msg:
            context.set_state("mental_mode", None)
            return "💙 Mental Health Support closed. I'm always here if you need me."

        return (
            "💙 I'm here for you.\n\n"
            "You can talk to me about stress, anxiety, sadness, or anything on your mind.\n"
            "Take your time — I'm listening."
        )
