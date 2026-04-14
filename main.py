from dotenv import load_dotenv
load_dotenv()
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from db.database import init_db
from app.agent.graph import agent

app = FastAPI(title="Smart Support Agent")

class UserMessage(BaseModel):
    message: str
    session_id: str=None

@app.on_event("startup")
def startup():
    init_db()

@app.post("/chat")
def chat(body: UserMessage):
    session_id = body.session_id or str(uuid.uuid4())
    initial_state = {
        "user_input": body.message,
        "intent": "",
        "entities": {},
        "missing_fields": [],
        "retrieved_docs": [],
        "tool_output": {},
        "response": "",
        "escalation": False,
        "messages": [],
        "session_id": session_id
    }
    result = agent.invoke(initial_state)
    return {
        "response": result["response"],
        "intent": result["intent"],
        "session_id": session_id
    }
