from langgraph.prebuilt.chat_agent_executor import AgentState
from typing import Optional

class MainState(AgentState):
    active_agent: Optional[str]
    phone_number: str
    is_authorized: bool
    otp_sent: bool
    customer_id: Optional[str]
    welcome_message: Optional[str]
