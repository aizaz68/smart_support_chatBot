from typing import TypedDict

class AgentState(TypedDict):
    user_input: str
    intent: str
    entities: dict
    missing_fields: list
    retrieved_docs: list
    tool_output: dict
    response: str
    escalation: bool
