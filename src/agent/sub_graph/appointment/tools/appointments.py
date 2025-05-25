from typing import Annotated
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
import json
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId
from agent.state import CustomState
from typing import Literal
from langchain_core.tools import tool
from agent.utils.node_names import NodeName
from langgraph_swarm import create_handoff_tool

def get_appointments(state: Annotated[CustomState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):   
   """
   Get appointments for a given customer ID.

   returns is json string of list of appointments or empty list if no appointments are found
   """
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

@tool(
   'welcome_message',
   description="""
   It is used to send the welcome message to the user.
   """)
def welcome_message(
   state: Annotated[CustomState, InjectedState], 
   tool_call_id: Annotated[str, InjectedToolCallId]
):
   welcome_message = "Hello, I am your Ai assistant. I can help you with your appointment and order related queries."
   tool_message = ToolMessage(content=welcome_message, tool_call_id=tool_call_id)
   
   return Command(update={"messages": state['messages'] + [tool_message]})


transfer_to_idv_agent = create_handoff_tool(
   agent_name=NodeName.idv_agent.value,
   description=f"Transfer user to the {NodeName.idv_agent.value} assistant."
)

transfer_to_order_agent = create_handoff_tool(
   agent_name=NodeName.order_agent.value,
   description=f"Transfer user to the {NodeName.order_agent.value} assistant."
)

   