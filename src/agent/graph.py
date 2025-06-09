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

graph = (
	create_swarm(
		agents=[
			*VirtualAgentBuilder.build(virtual_agent)
		],
		default_active_agent='provider_agent',
		state_schema=MainState,
		config_schema=Configuration,
	).compile(name='swarm_graph')
)
