from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.agent.state import AgentState
from app.tools.tools import (
    retrieve_company_knowledge,
    book_appointment,
    create_support_ticket,
    send_confirmation,
    check_calendar_availability
)

llm = ChatOpenAI(model="gpt-4o-mini")

def classify_intent(state: AgentState) -> AgentState:
    response = llm.invoke([
        SystemMessage(content="""
You are an intent classifier. Classify the user input into one of these intents:
- rag: user is asking a general question about the company
- booking: user wants to book an appointment
- ticket: user wants to report an issue or complaint
- escalation: user is angry or the issue is complex

Reply with only the intent word.
"""),
        HumanMessage(content=state["user_input"])
    ])
    state["intent"] = response.content.strip().lower()
    return state

def retrieve_knowledge(state: AgentState) -> AgentState:
    docs = retrieve_company_knowledge(state["user_input"])
    state["retrieved_docs"] = docs
    return state

def generate_rag_response(state: AgentState) -> AgentState:
    context = "\n\n".join([doc["content"] for doc in state["retrieved_docs"]])
    response = llm.invoke([
        SystemMessage(content=f"""
You are a helpful support agent for ScalableTech Solutions.
Use ONLY the context below to answer.
If the answer is not in the context, say you don't know.

Context:
{context}
"""),
        HumanMessage(content=state["user_input"])
    ])
    state["response"] = response.content
    return state

def collect_entities(state: AgentState) -> AgentState:
    response = llm.invoke([
        SystemMessage(content="""
Extract booking details from the user input.
Return a JSON object with these keys: name, email, datetime.
If a field is missing, set its value to null.
Reply with only the JSON.
"""),
        HumanMessage(content=state["user_input"])
    ])
    import json
    try:
        state["entities"] = json.loads(response.content)
    except:
        state["entities"] = {"name": None, "email": None, "datetime": None}

    missing = [k for k, v in state["entities"].items() if not v]
    state["missing_fields"] = missing
    return state

def execute_booking(state: AgentState) -> AgentState:
    e = state["entities"]
    result = book_appointment(e["name"], e["email"], e["datetime"])
    send_confirmation(result)
    state["tool_output"] = result
    state["response"] = f"Appointment booked for {e['name']} on {e['datetime']}. Confirmation sent to {e['email']}."
    return state

def execute_ticket(state: AgentState) -> AgentState:
    result = create_support_ticket(state["user_input"])
    state["tool_output"] = result
    state["response"] = f"Support ticket #{result['ticket_id']} created. Our team will reach out shortly."
    return state

def handle_escalation(state: AgentState) -> AgentState:
    state["escalation"] = True
    state["response"] = "I'm escalating your issue to a human agent. Someone will contact you shortly."
    return state

def ask_missing_fields(state: AgentState) -> AgentState:
    fields = ", ".join(state["missing_fields"])
    state["response"] = f"I need a few more details to book your appointment. Please provide: {fields}."
    return state
