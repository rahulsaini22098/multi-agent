"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from typing import TypedDict

from agent.state import MainState     
from langgraph_swarm import create_swarm
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
