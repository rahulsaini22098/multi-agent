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
   'handoff_to_idv_agent', 
   description="""
   It is used to transfer the control to idv agent.
   - IDV Agent is responsible for handling the user (authentication and authorization).
      such as 
      - validate payload
      - send otp
      - verify otp
      - confirm authorization
      - set phone number
   """)
def handoff_to_idv_agent(
      state: Annotated[CustomState, InjectedState], 
      tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command[Literal["idv_agent"]]:
   
   tool_message = ToolMessage(content="transfer to idv agent", tool_call_id=tool_call_id)
   
   return Command(
      goto=NodeName.idv_agent.value,
      graph=Command.PARENT,
      update={
         "messages": state['messages'] + [tool_message]
      }  
   )
   
@tool(
   'handoff_to_order_agent', 
   description="""
   It is used to transfer the control to order agent.
   - Order Agent is responsible for handling the order related queries.
      such as 
      - List user orders
   """)
def handoff_to_order_agent(
      state: Annotated[CustomState, InjectedState], 
      tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command[Literal["order_agent"]]:
   
   tool_message = ToolMessage(content="transfer to order agent", tool_call_id=tool_call_id)
   
   return Command(
      goto=NodeName.order_agent.value,
      graph=Command.PARENT,
      update={
         "messages": state['messages'] + [tool_message]
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