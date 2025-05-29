from typing import List, Union, Callable
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import BaseTool
from agent.state import MainState
from langgraph.graph.graph import CompiledGraph
from langchain_openai import ChatOpenAI
from mock.agent import agent_config, AgentConfig
from langchain_core.messages import SystemMessage
from core.tools import all_tools
import re

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
    return sanitized.strip('_')

  
  def _build_system_prompt(self,state: MainState):
    print("build system prompt")
    
    system_prompt = f"""
    You are an intelligent assistant whose responsibilties is to answer the appointment related queries using the
      tool at you disposal in you best capacity.
      
      Appointment service we support are:
      {self._agent_services}
      
      Context:
       is_authorized: {state.get('is_authorized')}
      
      Instructions:
        - Before using **any appointment-related tool**, you **must check if `is_authorized` is True**.
          - If `is_authorized` is **False**, you **must first call** the tool: `handoff_to_idv_agent`.
          - Only after the user is successfully authenticated should you proceed with any appointment tools like `get_appointments`.
                  
        - If user ask about anyhting else apart from appointment related queries whose intent matched with the description 
          of these tool at your disposal then you should call one of these tool. Only initiate one handoff at a time. 
          The tools are:
          1. handoff_to_order_agent

        - If user send any greeting message eg. hey, hello or any other greeting message or message whose intent is to know about the services, 
          call the `welcome_message` tool.
        
        - Always make sure the last message should be the well structured ai response what can we show to user.
          Do not disclose and sensative information to user.
        
        - Do not make the parallel tool call only one at a time.
      
      Multi-Intent Handling:
        - If the user’s request mentions **appointments** plus any other service (e.g., orders), you **must**:
            1. **First**, invoke the relevant appointment-related tool (e.g., `get_appointments`) and wait for its result once flow is complete.
            2. **Then**, examine the user’s message to determine if it matches the purpose of any available handoff tools:
              - If it matches, invoke the appropriate handoff tool from the list below.
              - If no handoff tool matches, and the message indicates the user is asking about something unrelated to your scope, 
                hand off back to the agent you were transferred from.

        Available handoff tools:
        - `handoff_to_order_agent`

      Do not infer or reuse appointment or other service data from older message history. 
      Treat each tool call independently and based only on the current message context.
      parallel tool call is not allowed.  
    """
    
    return [SystemMessage(content=system_prompt)] + state["messages"]
  
  
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
  
  
  def _create_agent(self, name: str, prompt: Union[str, Callable], agent_config: AgentConfig) -> CompiledGraph:
    print(f"AgentBuilder: initilizing agent")
    
    configured_tools = self._build_tools(configured_tools=agent_config["configured_tools"])
    
    # create agent graph
    agent_graph: CompiledGraph = create_react_agent(
      model=ChatOpenAI(model="gpt-4o-mini"),
      tools=[*configured_tools, *self._handoff_tools],
      state_schema=MainState,
      name=self.sanitize_string(name),
      prompt=prompt,
    )
    
    return agent_graph
  
  
  def build(self, name: str, prompt: Union[str, Callable], agent_config: AgentConfig, ) -> CompiledGraph:
    print(f"AgentBuilder: Building agent {name}")
    
    agent_graph = self._create_agent(name, prompt, agent_config)
    
    print(f"AgentBuilder: Agent {name} built successfully")
    
    return agent_graph
    
    
    