from mock.virtual_agent import VirtualAgent
from mock.agent import AgentConfig, agents
from core.agent_builder.agent_builder import AgentBuilder
from langgraph.graph.graph import CompiledGraph
from utils.utils import create_handoff_tool
from core.idv_builder.idv_builder import IDVBuilder
from langchain_core.tools import BaseTool

class VirtualAgentBuilder:
    def __init__(self, virtual_agent: VirtualAgent, agents: list[AgentConfig]):
        self.virtual_agent: VirtualAgent = virtual_agent
        self.agents: list[AgentConfig] = agents
        self.default_handoff_tools: list[BaseTool] = []
        self.default_agents: list[CompiledGraph] = []
    
    @classmethod
    def build(cls, virtual_agent: VirtualAgent) -> list[CompiledGraph]:
        print(f"VirtualAgentBuilder: building virtual agent")
        
        configured_agents = virtual_agent.get("configured_agent_ids")
        fetched_agents: list[AgentConfig] = [agent for agent in agents if agent.get("agent_id") in configured_agents]

        instance = cls(virtual_agent, fetched_agents)
        
        return instance._build_agents()
    
    def _build_handoff_tools(self, agent_names: list[str]):
        print(f"VirtualAgentBuilder: building handoff tools for agents: {agent_names}")
        handoff_tools = []
        
        for agent_name in agent_names:
            handoff_tool = create_handoff_tool(
                agent_name=agent_name,
                description=f"Transfer user to the {agent_name} assistant."
            )
            handoff_tools.append(handoff_tool)
        
        print(f"VirtualAgentBuilder: handoff tools built successfully")
        
        return handoff_tools

    def _build_agent_graph(self, agent: AgentConfig):
        print(f"VirtualAgentBuilder: building agent graph for agent: {agent.get('agent_id')} name {agent.get('display_name')}")
        
        agent_builder = AgentBuilder()
        
        other_agent_names = [AgentBuilder.sanitize_string(other_agent.get("display_name")) for other_agent in agents if other_agent.get("agent_id") != agent.get("agent_id")]
        handoff_tools = self._build_handoff_tools(other_agent_names)  
        
        agent_builder.set_handoff_tools([*handoff_tools, *self.default_handoff_tools])
        
        agent_graph = agent_builder.build(
            name=agent.get("display_name"), 
            agent_config=agent
        )
        
        print(f"VirtualAgentBuilder: agent graph built successfully")
        
        return agent_graph
    
    def initilize_idv_agent(self):
        print(f"VirtualAgentBuilder: initializing idv agent")
        
        protected_agents = [agent for agent in self.agents if agent.get("needs_verification") == True]
        
        if len(protected_agents) > 0:
            idv_agent, transfer_to_idv_agent = IDVBuilder(protected_agents).build()
            
            self.default_agents.append(idv_agent)
            self.default_handoff_tools.append(transfer_to_idv_agent)            
                    
        print(f"VirtualAgentBuilder: idv agent initialized successfully")
        
        return True
    
    def _build_agents(self) -> list[CompiledGraph]:
        compiled_agent_graphs: list[CompiledGraph] = []
        
        self.initilize_idv_agent()
        
        for agent in self.default_agents:
            compiled_agent_graphs.append(agent)
        
        for agent in self.agents:
            print(f"VirtualAgentBuilder: building agent: {agent.get('agent_id')}, name: {agent.get('display_name')}")
            
            agent_graph = self._build_agent_graph(agent)
            
            print(f"VirtualAgentBuilder: agent id {agent.get('agent_id')}, name: {agent.get('display_name')} built successfully")
            
            compiled_agent_graphs.append(agent_graph)
            
        print(f"VirtualAgentBuilder: agents built successfully")
        
        return compiled_agent_graphs
    
    