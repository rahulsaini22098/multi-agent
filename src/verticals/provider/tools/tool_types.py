from typing import Literal, TypedDict
from langchain_core.tools import BaseTool
from core.tools.tool_types import ToolDefinition

WELCOME_MESSAGE = 'welcome_message'
GET_APPOINTMENTS = 'get_appointments'
TRANSFER_TO_IDV_AGENT = 'transfer_to_idv_agent'
TRANSFER_TO_ORDER_AGENT = 'transfer_to_order_agent'

ALL_TOOL_NAMES = [
    WELCOME_MESSAGE,
    GET_APPOINTMENTS,
    TRANSFER_TO_IDV_AGENT,
    TRANSFER_TO_ORDER_AGENT,
]

ToolName = Literal[
    'welcome_message',
    'get_appointments',
    'transfer_to_idv_agent',
    'transfer_to_order_agent',
]

class ProviderToolsJson(TypedDict):
    welcome_message: ToolDefinition
    get_appointments: ToolDefinition

class ProviderHandoffToolsJson(TypedDict):
    transfer_to_idv_agent: BaseTool 
    transfer_to_order_agent: BaseTool
