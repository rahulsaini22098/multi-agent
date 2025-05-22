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

@tool('handoff_to_idv_agent', description=" tool to transfer the control to idv agent")
def handoff_to_idv_agent(
      state: Annotated[CustomState, InjectedState], 
      tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command[Literal["idv_agent"]]:
   cleaned = [m for m in state['messages'] if m.type != "system"]
   
   tool_message = ToolMessage(content="transfer to idv agent", tool_call_id=tool_call_id)
   cleaned.append(tool_message)
   
   return Command(
      goto=NodeName.idv_agent.value,
      graph=Command.PARENT,
      update={
         "messages": cleaned
      }  
   )