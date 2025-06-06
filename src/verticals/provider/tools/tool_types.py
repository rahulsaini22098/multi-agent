from typing import Literal, TypedDict
from core.tools.tool_types import ToolDefinition

WELCOME_MESSAGE = 'welcome_message'
GET_APPOINTMENTS = 'get_appointments'
BOOK_APPOINTMENT = 'book_appointment'
CONFIRM_APPOINTMENT = 'confirm_appointment'
CANCEL_APPOINTMENT = 'cancel_appointment'
RESCHEDULE_APPOINTMENT = 'reschedule_appointment'

ALL_TOOL_NAMES = [
    WELCOME_MESSAGE,
    GET_APPOINTMENTS,
    BOOK_APPOINTMENT,
    CONFIRM_APPOINTMENT,
    CANCEL_APPOINTMENT,
    RESCHEDULE_APPOINTMENT,
]

ToolName = Literal[
    'welcome_message',
    'get_appointments',
    'book_appointment',
    'confirm_appointment',
    'cancel_appointment',
    'reschedule_appointment',
]

class ProviderToolsJson(TypedDict):
    welcome_message: ToolDefinition
    get_appointments: ToolDefinition
    book_appointment: ToolDefinition
    confirm_appointment: ToolDefinition
    cancel_appointment: ToolDefinition
    reschedule_appointment: ToolDefinition
    
class RetailToolsJson(TypedDict):
    get_orders: ToolDefinition
