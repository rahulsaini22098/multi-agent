from langgraph.prebuilt.chat_agent_executor import AgentState
from typing import Optional
from typing import Annotated
import operator
class CustomState(AgentState):
    active_agent: Optional[str]
    phone_number: Annotated[str, "9876543210"]
    is_authorized: bool
    otp_sent: bool
    customer_id: Optional[str]
