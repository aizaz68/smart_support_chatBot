from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    user_input: str
    intent: str
    entities: dict
    missing_fields: list
    retrieved_docs: list
    tool_output: dict
    response: str
    escalation: bool
    messages: Annotated[list[BaseMessage], operator.add]  
    session_id: str                                        