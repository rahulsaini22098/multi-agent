from langgraph.prebuilt.chat_agent_executor import AgentState
from typing import Optional
from typing import Annotated
import operator
class CustomState(AgentState):
    phone_number: Annotated[str, "9876543210"] = "9876543210"
    is_authorized: bool = False
    otp_sent: bool = False
    customer_id: Optional[str] = None
