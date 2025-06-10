from verticals.banking.tools.tools import authenticate_user, get_balance, transfer_money, deduct_amount
from verticals.banking.tool_types import BankingToolsJson

banking_tools_json: BankingToolsJson = {
    "authenticate_user": {
        "description": "Authenticate user and authorize for banking operations",
        "tool": authenticate_user
    },
    "get_balance": {
        "description": "Get customer's total balance",
        "tool": get_balance
    },
    "transfer_money": {
        "description": "Transfer money to another account",
        "tool": transfer_money
    },
    "deduct_amount": {
        "description": "Deduct an amount from customer's account",
        "tool": deduct_amount
    }
}
