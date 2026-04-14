from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import (
    classify_intent,
    retrieve_knowledge,
    generate_rag_response,
    collect_entities,
    execute_booking,
    execute_ticket,
    handle_escalation,
    ask_missing_fields,
    log_and_respond,
)

def route_intent(state: AgentState) -> str:
    intent = state["intent"]
    if intent == "rag":
        return "rag"
    elif intent == "booking":
        return "booking"
    elif intent == "ticket":
        return "ticket"
    else:
        return "escalation"

def route_booking(state: AgentState) -> str:
    if state["missing_fields"]:
        return "ask"
    return "execute"

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_knowledge", retrieve_knowledge)
    graph.add_node("generate_rag_response", generate_rag_response)
    graph.add_node("collect_entities", collect_entities)
    graph.add_node("execute_booking", execute_booking)
    graph.add_node("execute_ticket", execute_ticket)
    graph.add_node("handle_escalation", handle_escalation)
    graph.add_node("ask_missing_fields", ask_missing_fields)
    graph.add_node("log_and_respond", log_and_respond)

    graph.set_entry_point("classify_intent")

    graph.add_conditional_edges("classify_intent", route_intent, {
        "rag": "retrieve_knowledge",
        "booking": "collect_entities",
        "ticket": "execute_ticket",
        "escalation": "handle_escalation"
    })

    graph.add_edge("retrieve_knowledge", "generate_rag_response")
    graph.add_edge("generate_rag_response", "log_and_respond")

    graph.add_conditional_edges("collect_entities", route_booking, {
        "ask": "ask_missing_fields",
        "execute": "execute_booking"
    })

    graph.add_edge("ask_missing_fields", "log_and_respond")
    graph.add_edge("execute_booking", "log_and_respond")
    graph.add_edge("execute_ticket", "log_and_respond")
    graph.add_edge("handle_escalation", "log_and_respond")
    graph.add_edge("log_and_respond", END)

    return graph.compile()


agent = build_graph()
