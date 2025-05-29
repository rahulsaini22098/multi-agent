from typing import Annotated
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
import json
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId
from agent.state import MainState
from langchain_core.tools import tool
from utils.node_names import NodeName
from langgraph_swarm import create_handoff_tool


@tool(
   'welcome_message',
   description="""
   It is used to send the welcome message to the user.
   """)
def welcome_message(
   state: Annotated[MainState, InjectedState], 
   tool_call_id: Annotated[str, InjectedToolCallId]
):
   welcome_message = state["welcome_message"] or "Hello, I am your Ai assistant. I can help you with your appointment and order related queries."
   tool_message = ToolMessage(content=welcome_message, tool_call_id=tool_call_id)
   
   return Command(update={"messages": state['messages'] + [tool_message]})
 
 
@tool('get_appointments', 
      description="""It is used to get all the appointments of the customer"""
)
def get_appointments(
  state: Annotated[MainState, InjectedState], 
  tool_call_id: Annotated[str, InjectedToolCallId]
):   
  print(f"Looking up appointment for customer {state['customer_id']}")
  customer_id = state['customer_id']
  
  if customer_id == "101":
    appointments = json.dumps([
        {
          "appointment_id": "101-1",
          "appointment_date": "2024-01-01",
          "appointment_time": "10:00 AM"
        },
        {
          "appointment_id": "101-2",
          "appointment_date": "2024-01-02",
          "appointment_time": "11:00 AM"
        }
    ])

    return Command(
        update={
          "messages": state['messages'] + [
              ToolMessage(content=appointments, tool_call_id=tool_call_id)
          ]
        }
    )
  else:
    return Command(
        update={
          "messages": state['messages'] + [
              ToolMessage(content=json.dumps([]), tool_call_id=tool_call_id)
          ]
        }
    )


transfer_to_idv_agent = create_handoff_tool(
   agent_name=NodeName.idv_agent.value,
   description=f"Transfer user to the {NodeName.idv_agent.value} assistant."
)

transfer_to_order_agent = create_handoff_tool(
   agent_name=NodeName.order_agent.value,
   description=f"Transfer user to the {NodeName.order_agent.value} assistant."
)