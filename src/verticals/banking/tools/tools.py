from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from langchain_core.tools import InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from agent.state import MainState
from mock.banking import get_banking_store
import json

store = get_banking_store()

@tool("authenticate_user", description="Authenticate user and authorize banking operations")
def authenticate_user(
    state: Annotated[MainState, InjectedState],
    phone_number: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    # Simulate OTP authentication
    msg = f"OTP sent to {phone_number} and user authenticated successfully."
    return Command(
        update={
            "is_authorized": True,
            "customer_id": phone_number,
            "messages": state["messages"] + [
                ToolMessage(content=msg, tool_call_id=tool_call_id)
            ],
        }
    )

@tool("get_balance", description="Get customer's total balance")
def get_balance(
    state: Annotated[MainState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    if not state.get("is_authorized"):
        msg = "User not authorized. Please authenticate first."
        return Command(
            update={
                "messages": state["messages"] + [
                    ToolMessage(content=msg, tool_call_id=tool_call_id)
                ]
            }
        )
    customer = store.get_customer(state["customer_id"])
    if customer is None:
        msg = "Customer not found."
    else:
        total = customer.get("total_balance", 0.0)
        msg = json.dumps({"total_balance": total})
    return Command(
        update={
            "messages": state["messages"] + [
                ToolMessage(content=msg, tool_call_id=tool_call_id)
            ]
        }
    )

@tool("transfer_money", description="Transfer money to another account")
def transfer_money(
    state: Annotated[MainState, InjectedState],
    target_account: str,
    amount: float,
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    if not state.get("is_authorized"):
        msg = "User not authorized. Please authenticate first."
        return Command(
            update={
                "messages": state["messages"] + [
                    ToolMessage(content=msg, tool_call_id=tool_call_id)
                ]
            }
        )
    customer = store.get_customer(state["customer_id"])
    if not customer:
        msg = "Customer not found."
        return Command(update={"messages": state["messages"] + [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    accounts = customer.get("accounts", [])
    if not accounts:
        msg = "No accounts available for customer."
        return Command(update={"messages": state["messages"] + [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    source_acc = accounts[0]
    src_no = source_acc["account_number"]
    src_balance = source_acc["balance"]
    if src_balance < amount:
        msg = "Insufficient funds."
        return Command(update={"messages": state["messages"] + [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    target = store.get_account(target_account)
    if not target:
        msg = "Target account not found."
        return Command(update={"messages": state["messages"] + [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    # perform transfer
    store.update_account_balance(src_no, src_balance - amount)
    tgt_balance = target["balance"] + amount
    store.update_account_balance(target_account, tgt_balance)
    msg = f"Transferred {amount} from {src_no} to {target_account}."
    return Command(update={"messages": state["messages"] + [ToolMessage(content=json.dumps({"new_balance": src_balance - amount}), tool_call_id=tool_call_id)]})

@tool("deduct_amount", description="Deduct amount from customer's account")
def deduct_amount(
    state: Annotated[MainState, InjectedState],
    amount: float,
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    if not state.get("is_authorized"):
        msg = "User not authorized. Please authenticate first."
        return Command(update={"messages": state["messages"] + [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    customer = store.get_customer(state["customer_id"])
    if not customer:
        msg = "Customer not found."
        return Command(update={"messages": state["messages"] + [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    accounts = customer.get("accounts", [])
    if not accounts:
        msg = "No accounts available for customer."
        return Command(update={"messages": state["messages"] + [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    source_acc = accounts[0]
    src_no = source_acc["account_number"]
    src_balance = source_acc["balance"]
    if src_balance < amount:
        msg = "Insufficient funds."
        return Command(update={"messages": state["messages"] + [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    # deduct
    store.update_account_balance(src_no, src_balance - amount)
    msg = f"Deducted {amount} from {src_no}."
    return Command(update={"messages": state["messages"] + [ToolMessage(content=json.dumps({"new_balance": src_balance - amount}), tool_call_id=tool_call_id)]})
