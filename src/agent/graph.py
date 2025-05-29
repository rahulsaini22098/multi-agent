"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from typing import TypedDict
from langgraph.graph import StateGraph
from agent.state import MainState     
from agent.sub_graph.agent_manager.agent_manager import AgentManager
from langgraph.graph import START
from utils.node_names import NodeName 
from agent.sub_graph.idv.idv import IDVAgent
from agent.sub_graph.appointment.appointment import AppointmentAgent
from agent.sub_graph.order.order import OrderAgent
from langgraph_swarm import create_swarm
from core.agent_builder.agent_builder import AgentBuilder

class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    model_name: str
    recursion_limit: int
    thread_id: int


graph = (
    create_swarm(
        agents=[
            AppointmentAgent.build_agent(),
            # OrderAgent.create_agent(), 
            IDVAgent.create_agent()
        ],
        default_active_agent='provider_agent',
        state_schema=MainState,
        config_schema=Configuration,
    ).compile(name='main_graph')
)
