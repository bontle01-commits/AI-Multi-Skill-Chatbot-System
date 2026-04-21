from Skills.Base import Skill, SessionLocal
from sqlalchemy import Column, Integer, String
from Skills.Base import Base

class TechSupportEntry(Base):
    __tablename__ = "tech_support"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    response = Column(String, nullable=False)

class TechSupport(Skill):
    def can_handle(self, user_input, context):
        return context.get("intent") == "tech"

    def handle(self, user_input, context):
        msg = user_input.lower().strip()
        db = SessionLocal()

        if context.get_state("tech_mode") is None:
            context.set_state("tech_mode", "menu")
            db.close()
            return (
                "💻 Tech Support Activated\n\n"
                "I can help you fix technical issues step by step 🔧\n\n"
                "Choose an option:\n"
                "1. 🛠️ App not working / crashing\n"
                "2. ⚠️ Error messages\n"
                "3. 🐢 Slow performance\n"
                "4. 🌐 Internet / connection issues\n"
                "5. 🚪 Exit Tech Support\n\n"
                "Reply with a number (1–5)."
            )

        if context.get_state("tech_mode") == "menu":
            mapping = {
                "1": "App Not Working",
                "2": "Error Messages",
                "3": "Slow Performance",
                "4": "Internet Issues",
            }

            if msg in mapping:
                entry = db.query(TechSupportEntry).filter(TechSupportEntry.category == mapping[msg]).first()
                db.close()
                if entry:
                    return f"{entry.category}:\n\n{entry.response}"
                else:
                    return f"❗ No info found for {mapping[msg]}."
            elif msg == "5":
                context.set_state("tech_mode", None)
                db.close()
                return "🚪 Tech Support closed. Ask me anything else 💻"
            else:
                db.close()
                return "❗ Please choose a valid option (1–5)."

        db.close()
        return "💻 Say 'error', 'bug', or 'issue' to start Tech Support."
