from Skills.Base import Skill, SessionLocal
from sqlalchemy import Column, Integer, String
from  Skills.Base import Base


class FAQ(Base):
    __tablename__ = "faq"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    content = Column(String, nullable=False)



class UniversityFAQ(Skill):
    def can_handle(self, user_input, context):
        
        return context.get("intent") == "faq"

    def handle(self, user_input, context):
        msg = user_input.lower().strip()
        db = SessionLocal()

        if context.get_state("faq_mode") is None:
            context.set_state("faq_mode", "menu")
            db.close()
            return (
                "🎓 University FAQ Assistant\n\n"
                "I can help you with university-related questions.\n\n"
                "Choose an option:\n"
                "1. 📌 Admissions\n"
                "2. 💰 Fees\n"
                "3. 📚 Courses\n"
                "4. ⏰ Deadlines\n"
                "5. 🚪 Exit FAQ\n\n"
                "Reply with a number (1–5)."
            )

        if context.get_state("faq_mode") == "menu":
            mapping = {
                "1": "Admissions",
                "2": "Fees",
                "3": "Courses",
                "4": "Deadlines",
            }

            if msg in mapping:
                faq_entry = db.query(FAQ).filter(FAQ.category == mapping[msg]).first()
                db.close()
                if faq_entry:
                    return f"{faq_entry.category} Information:\n\n{faq_entry.content}"
                else:
                    return f"❗ No info found for {mapping[msg]}."
            elif msg == "5":
                context.set_state("faq_mode", None)
                db.close()
                return "🚪 FAQ mode closed. Ask me anything else 🎓"
            else:
                db.close()
                return "❗ Please choose a valid option (1–5)."

        db.close()
        return "🎓 Say 'admission', 'fees', 'courses', or 'deadline' to start FAQ help."
