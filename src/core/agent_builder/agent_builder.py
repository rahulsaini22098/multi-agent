from typing import List, Union, Callable
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import BaseTool
from agent.state import MainState
from langgraph.graph.graph import CompiledGraph
from langchain_openai import ChatOpenAI
from mock.agent import AgentConfig, Vertical
from langchain_core.messages import SystemMessage
from core.tools import all_tools
import re
from verticals.provider.prompts.prompts import agent_prompt

class AgentBuilder:
  _agent_services: list[str] = []
  
  @staticmethod
  def sanitize_string( value: str) -> str:
    """
    Replace all special characters and spaces in a string with underscores.
    
    Examples:
        "ahbsdh sujbjsb" → "ahbsdh_sujbjsb"
        "provider-agent" → "provider_agent"
        "pr-787(&&*-agent world" → "pr_787_agent_world"
    """
    # Replace all non-alphanumeric characters with underscores
    sanitized = re.sub(r'[^A-Za-z0-9]+', '_', value)
    # Strip leading/trailing underscores
    return sanitized.strip('_').lower()

  
  def _build_system_prompt(self):
    print("AgentBuilder: build system prompt")
    
    def system_prompt(state: MainState):
      
      system_prompt = agent_prompt(state, self._agent_services)

      return [SystemMessage(content=system_prompt)] + state["messages"]
    
    return system_prompt
  
  
  def _build_tools(self, configured_tools: List[str]):
    tools: List[BaseTool] = []
    
    self._agent_services = []
    for tool_name in configured_tools:
      if tool_name in all_tools:
        tools.append(all_tools[tool_name]["tool"])
        self._agent_services.append(f"- {all_tools[tool_name]['description']} (via the `{tool_name}` tool)")
      else:
        print(f"AgentBuilder: Tool {tool_name} not found in all_tools")
    
    return tools
  
  
  
  def set_handoff_tools(self, handoff_tools: List[BaseTool]):
    self._handoff_tools = handoff_tools
    
    return self
  
  
  def _create_agent(self, name: str, agent_config: AgentConfig) -> CompiledGraph:
    print(f"AgentBuilder: initilizing agent")
    
    configured_tools = self._build_tools(configured_tools=agent_config["configured_tools"])
    
    # create agent graph
    agent_graph: CompiledGraph = create_react_agent(
      model=ChatOpenAI(model="gpt-4o-mini"),
      tools=[*configured_tools, *self._handoff_tools],
      state_schema=MainState,
      name=self.sanitize_string(name),
      prompt=self._build_system_prompt(),
    )
    
    return agent_graph
  
  
  def build(self, name: str, agent_config: AgentConfig) -> CompiledGraph:
    print(f"AgentBuilder: Building agent name: {self.sanitize_string(name)}")
    
    agent_graph = self._create_agent(name, agent_config)
    
    print(f"AgentBuilder: Agent name: {self.sanitize_string(name)} built successfully")
    
    return agent_graph
    
    
    