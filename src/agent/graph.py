"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from typing import TypedDict
from langgraph.graph import StateGraph
from agent.state import CustomState     
from agent.sub_graph.agent_manager.agent_manager import AgentManager
from langgraph.graph import START
from agent.utils.node_names import NodeName 
from agent.sub_graph.idv.idv import IDVAgent
from agent.sub_graph.appointment.appointment import AppointmentAgent
from agent.sub_graph.order.order import OrderAgent

class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    model_name: str
    recursion_limit: int
    thread_id: int


graph = (

    #  Graph using supervisor
    StateGraph(CustomState, config_schema=Configuration)
    .add_node(NodeName.agent_manager.value, AgentManager.compile_graph())

    # Add edges
    .add_edge(START, NodeName.agent_manager.value)

    # compile the graph
    .compile(name='main_graph')

    # Graph using react agent
    # StateGraph(CustomState, config_schema=Configuration)
    # .add_node(NodeName.agent_manager.value, AgentManager.create_agent())
    # .add_node(NodeName.idv_agent.value, IDVAgent.create_agent())
    # .add_node(NodeName.appointment_agent.value, AppointmentAgent.create_agent())
    # .add_node(NodeName.order_agent.value, OrderAgent.create_agent())


    # # Add edges
    # .add_edge(START, NodeName.agent_manager.value)
    # .compile(name='main_graph')
)
