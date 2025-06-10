from typing import Literal, TypedDict
from core.tools.tool_types import ToolDefinition

# Tool names for Banking vertical
AUTHENTICATE_USER = 'authenticate_user'
GET_BALANCE = 'get_balance'
TRANSFER_MONEY = 'transfer_money'
DEDUCT_AMOUNT = 'deduct_amount'

ALL_TOOL_NAMES = [
    AUTHENTICATE_USER,
    GET_BALANCE,
    TRANSFER_MONEY,
    DEDUCT_AMOUNT,
]

ToolName = Literal[
    'authenticate_user',
    'get_balance',
    'transfer_money',
    'deduct_amount',
]

class BankingToolsJson(TypedDict):
    authenticate_user: ToolDefinition
    get_balance: ToolDefinition
    transfer_money: ToolDefinition
    deduct_amount: ToolDefinition
