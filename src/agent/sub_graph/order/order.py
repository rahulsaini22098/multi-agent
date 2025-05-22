from langchain_openai import ChatOpenAI
from agent.state import CustomState
from agent.utils.node_names import NodeName
from langgraph_supervisor import create_supervisor
from agent.sub_graph.idv.idv import IDVAgent
from langgraph.prebuilt import create_react_agent
from agent.sub_graph.order.tools.order import get_order, handoff_to_idv_agent
from langchain_core.messages import SystemMessage

class OrderAgent:

  @staticmethod
  def agent_prompt(state: CustomState):

    if state.get('is_authorized') is None or state.get('is_authorized') == False:
      system_prompt = f"""
      Its look like you are not authorized to manage orders.
      call the handoff_to_idv_agent tool initiate the authroization flow so user can manage appointments.
      """
    
    else:
      system_prompt = f"""
      You are an expert agent who's sole and only purpose and responsibility is to handle the order related queries.

      These are the the feature you currently support:
      1. List user orders

      If user asks about anything else, you should politely decline and say you support only the above features.

      You should only continue with the listed features if user is already authorised.

      Always make sure the last message should be the well structured ai response what can we shouw to user.
      Do not disclose and sensative information to user.
    """

    return [SystemMessage(content=system_prompt)] + state['messages']
  
  @staticmethod
  def create_agent():
    order_agent = create_react_agent(
      model=ChatOpenAI(model="gpt-4o-mini"),
      state_schema=CustomState,
      tools=[get_order],
      prompt=OrderAgent.agent_prompt_for_supervisor,
      name=NodeName.order_agent.value
    )

    return order_agent
  
  @staticmethod
  def agent_prompt_for_supervisor(state: CustomState):
    
    if state.get('is_authorized') is None or state.get('is_authorized') == False:
      system_prompt = f"""
      Its look like you are not authorized to manage orders.supervisor need to handoff the control to idv agent to authenticate the user first.
      
      Do not make any tool call related to orders.
      """
    
    else:
      system_prompt = f"""
      You are an expert agent who's sole and only purpose and responsibility is to handle the order related queries.

      These are the the feature you currently support:
      1. List user orders

      If user asks about anything else, you should politely decline and say you support only the above features.

      You should only continue with the listed features if user is already authorised.

      Always make sure the last message should be the well structured ai response what can we shouw to user.
      Do not disclose and sensative information to user.
    """

    return [SystemMessage(content=system_prompt)] + state['messages']
  
  @staticmethod
  def compile_graph():
    
    workflow = create_supervisor(
        tools=[],
        agents=[IDVAgent.create_agent()],
        model=ChatOpenAI(model="gpt-4o-mini"),
        state_schema=CustomState,
        prompt=OrderAgent.agent_prompt_for_supervisor,
        supervisor_name="order_agent_supervisor",
        output_mode="full_history"
    )

    return workflow.compile(name=NodeName.order_agent.value)