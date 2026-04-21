from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from router import Chatbot
from Context import Context

from Skills.FAQ import UniversityFAQ
from Skills.Mental_Health import MentalHealthSupport
from Skills.Travel import TravelPlanner
from Skills.Tech_Support import TechSupport

from database import (
    init_db,
    save_message,
    get_total_messages,
    get_intent_stats,
    get_recent_chats
)

app = FastAPI()

# ✅ Enable CORS (important for frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

skills = [
    UniversityFAQ(),
    MentalHealthSupport(),
    TravelPlanner(),
    TechSupport()
]

bot = Chatbot(skills)
context = Context()

class Message(BaseModel):
    text: str

@app.get("/")
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
def chat(message: Message):
    user_text = message.text

    response = bot.process(user_text, context)

    intent = context.get("intent")

    save_message(user_text, response, intent)

    return {"response": response}

@app.get("/analytics")
def analytics():
    return {
        "total_messages": get_total_messages(),
        "intent_stats": get_intent_stats()
    }

@app.get("/recent")
def recent():
    return get_recent_chats()