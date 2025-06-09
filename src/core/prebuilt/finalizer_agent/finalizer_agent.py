from agent.state import MainState
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from utils.utils import create_handoff_tool
from langchain_core.tools import BaseTool
from langgraph.types import Command
from langgraph.graph import END
from langgraph.prebuilt import InjectedState
from langchain_core.tools import InjectedToolCallId
from typing import Annotated
from langchain_core.messages import ToolMessage

class FinalizerAgent:
  _tools: list[BaseTool] = []
    
  def build_prompt(self):

      def agent_prompt(state: MainState) -> str:
        print(f"PlannerAgent: building planner agent prompt")
        
        system_prompt = f"""
        You are an intelligent assistant who is responsible to determine if the user query is answered 
        or should we continue the conversation using the `finalizer_tool`.
        
        Important Rules:
         - You do not response back to user.
        """
        
        return system_prompt
      
      return agent_prompt
  
  def _get_handoff_tool(self):
    handoff_tool = create_handoff_tool(
      agent_name="finalizer_agent",
      description=""" transfer to the finalizer_agent to determine if the user query is answered or should we continue the conversation """,
    )
    
    return handoff_tool
  
  def _initialize_tools(self):
    
    def finalizer_tool(
      redirect_to: str,
      state: Annotated[MainState, InjectedState],
      tool_call_id: Annotated[str, InjectedToolCallId]
    ) -> Command:
      """
      A tool that is responsible to determine if the user query is answered or should we continue the conversation on theb
      basis on conversation history.
      
      Input
      redirect_to: str (the agent to redirect to if query is not answered or should we continue the conversation on the basis of conversation history
       value should be previous agent name called the finalizer_agen otherwise __end__
      )
      
      The `finalizer_tool` is a tool that is responsible to determine if the user query is answered or should we continue the conversation.
      
      """
      
      print(f"FinalizerAgent: finalizer tool called")
      
      tool_message = ToolMessage(
        content="user query is answered",
        tool_call_id=tool_call_id
      ) 
     
      return Command(
        goto=redirect_to,
        graph=Command.PARENT,
        update={
          "messages": state['messages'] + [tool_message]
        }
      )
    
    self._tools = [ finalizer_tool ]
  
  def build(self):
    
    self._initialize_tools()
    
    transfer_to_finalizer_agent = self._get_handoff_tool()
    
    finalizer_agent = create_react_agent(
        model=ChatOpenAI(model="gpt-4o-mini", temperature=0.0),
        name="finalizer_agent",
        tools=self._tools,
        prompt=self.build_prompt(),
        state_schema=MainState,
    )
    
    return finalizer_agent, transfer_to_finalizer_agent