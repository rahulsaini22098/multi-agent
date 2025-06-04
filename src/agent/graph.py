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
from core.virtual_agent_builder.virtual_agent_builder import VirtualAgentBuilder
from mock.virtual_agent import virtual_agent

class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    model_name: str
    recursion_limit: int
    thread_id: int
    
    
    """ 
     1. Get VA config on the basis of sender number from db.
     2. Get all agents associated with the VA config.
     3. creata a graph using Virtual AGent builder using VA config.
     4. call build and tal VA config as argument.
     
     
     eg agents ['provider_agent', 'idv_agent', 'order_agent']
    #  VA Builder
     1. Iterate  (Provider Agent) over configured agents and filter out the current agent and 
        create the handoof tools for each agent.
    2. If is_verficed is true then add idv in the handoff tools.
    3. create a AGentBUildert instance call handoff tools and build method.
    
    """


graph = (
    create_swarm(
        agents=[
            *VirtualAgentBuilder.build(virtual_agent)
            # AppointmentAgent.build_agent(),
            # # OrderAgent.create_agent(), 
            # IDVAgent.create_agent()
        ],
        default_active_agent='provider_agent',
        state_schema=MainState,
        config_schema=Configuration,
    ).compile(name='main_graph')
)
