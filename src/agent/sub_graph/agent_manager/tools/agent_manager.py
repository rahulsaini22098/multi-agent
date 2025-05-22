from langchain_core.tools import tool, InjectedToolCallId
from agent.state import CustomState
from typing import Literal
from langchain_core.tools import tool
from agent.utils.node_names import NodeName
from typing import Annotated
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain_core.messages import ToolMessage

@tool('handoff_to_appointment_agent', description=" tool to transfer the control to appointment agent")
def handoff_to_appointment_agent(
      state: Annotated[CustomState, InjectedState], 
      tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command[Literal["appointment_agent"]]:
   return Command(
      goto=NodeName.appointment_agent.value,
      graph=Command.PARENT,
      update={
         "messages": state['messages'] + [ToolMessage(content="tool to transfere the control to appointment agent", tool_call_id=tool_call_id)]
      }
   )

@tool('handoff_to_order_agent', description=" tool to transfer the control to order agent")
def handoff_to_order_agent(
      state: Annotated[CustomState, InjectedState], 
      tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command[Literal["order_agent"]]:
   return Command(
      goto=NodeName.order_agent.value,
      graph=Command.PARENT,
      update={
         "messages": state['messages'] + [ToolMessage(content="transfer to order agent", tool_call_id=tool_call_id)]
      }
   )