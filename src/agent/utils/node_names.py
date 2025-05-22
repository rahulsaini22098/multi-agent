from enum import Enum
class NodeName(Enum):
    welcome = 'welcome'
    supervisor_agent = 'supervisor_agent'
    interrupt = 'interrupt'
    agent_manager = 'agent_manager'
    order_agent = 'order_agent'
    appointment_agent = 'appointment_agent'
    idv_agent = 'idv_agent'
    normalize_state = 'normalize_state'