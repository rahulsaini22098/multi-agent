from langchain_core.tools import tool, InjectedToolCallId
from agent.state import CustomState
from typing import Literal
from langchain_core.tools import tool
from agent.utils.node_names import NodeName
from typing import Annotated
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain_core.messages import ToolMessage

order_data = [
  {
    "order_id": 1,
    "customer_id": 101,
    "order_date": "2025-05-20",
    "total_amount": 150.75,
    "status": "Shipped",
    "items": [
      {
        "item_id": "A1",
        "name": "Wireless Mouse",
        "quantity": 1,
        "price": 25.75
      },
      {
        "item_id": "A2",
        "name": "Mechanical Keyboard",
        "quantity": 1,
        "price": 125.00
      }
    ]
  },
  {
    "order_id": 2,
    "customer_id": 101,
    "order_date": "2025-05-21",
    "total_amount": 89.99,
    "status": "Processing",
    "items": [
      {
        "item_id": "B1",
        "name": "Laptop Stand",
        "quantity": 1,
        "price": 39.99
      },
      {
        "item_id": "B2",
        "name": "USB-C Hub",
        "quantity": 1,
        "price": 50.00
      }
    ]
  },
  {
    "order_id": 3,
    "customer_id": 102,
    "order_date": "2025-05-19",
    "total_amount": 200.00,
    "status": "Delivered",
    "items": [
      {
        "item_id": "C1",
        "name": "Smartwatch",
        "quantity": 1,
        "price": 200.00
      }
    ]
  },
  {
    "order_id": 4,
    "customer_id": 103,
    "order_date": "2025-05-18",
    "total_amount": 49.50,
    "status": "Cancelled",
    "items": [
      {
        "item_id": "D1",
        "name": "Notebook Set",
        "quantity": 3,
        "price": 16.50
      }
    ]
  },
  {
    "order_id": 5,
    "customer_id": 101,
    "order_date": "2025-05-22",
    "total_amount": 120.00,
    "status": "Pending",
    "items": [
      {
        "item_id": "E1",
        "name": "Bluetooth Speaker",
        "quantity": 2,
        "price": 60.00
      }
    ]
  }
]


@tool('get_order', description="Get the order for a given customer ID")
def get_order(
   state: Annotated[CustomState, InjectedState], 
   tool_call_id: Annotated[str, InjectedToolCallId]
  ):
   print(f"Looking up order for customer {state['customer_id']}")
   customer_id = state.get('customer_id', None)

   if customer_id == "101":
      filtered_orders = [order for order in order_data if customer_id == "101"]

      return Command(
         update={
            "messages": state['messages'] + [ToolMessage(content=f"Order found: {filtered_orders}", tool_call_id=tool_call_id)]
         }
      )
   else:
      return Command(
         update={
            "messages": state['messages'] + [ToolMessage(content="Order not found", tool_call_id=tool_call_id)]
         }
      )
   
@tool(
  'handoff_to_idv_agent', 
  description="""
  It is used to transfer the control to idv agent.
  - IDV Agent is responsible for handling the IDV (authentication and authorization) related queries.
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