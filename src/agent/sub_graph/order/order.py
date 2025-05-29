from langchain_openai import ChatOpenAI
from agent.state import MainState
from utils.node_names import NodeName
from langgraph_supervisor import create_supervisor
from agent.sub_graph.idv.idv import IDVAgent
from langgraph.prebuilt import create_react_agent
from agent.sub_graph.order.tools.order import get_order, transfer_to_idv_agent, transfer_to_appointment_agent
from langchain_core.messages import SystemMessage

class OrderAgent:

  @staticmethod
  def agent_prompt(state: MainState):
    
    system_prompt = f"""
      You are an expert agent who's sole and only purpose and responsibility is to handle the order related queries.

      Order service we support are:
      - List user orders (get_order tool)
      
      Context:
      is_authorized: {state.get('is_authorized')}
      
      Instructions:
      - Before using **any appointment-related tool**, you **must check if `is_authorized` is True**.
        - If `is_authorized` is ${state.get('is_authorized')}, you **must first call** the tool: `handoff_to_idv_agent`.
        - Only after the user is successfully authenticated should you proceed with any appointment tools like `get_appointments`.
      
      - If user ask about anyhting else apart from order services we have  whose intent matched with the description 
        of the handoff tool at your disposal then you should call one of those tool. 
        
        The tools are:
        1. handoff_to_appointment_agent
        
      - Always make sure the last message should be the well structured ai response what can we show to user.
        Do not disclose and sensative information to user.
      
      - Do not make the tool call in parallel. It should always be in sequence.
      
      Multi-Intent Handling:
        - If the user’s request mentions **orders** plus any other service (e.g., appointments), you **must**:
            1. **First**, invoke the relevant order-related tool (e.g., `get_order`) and wait for its result.
            2. **Then**, examine the user’s message to determine if it matches the purpose of any available handoff tools:
              - If it matches, invoke the appropriate handoff tool from the list below.
              - If no handoff tool matches, and the message indicates the user is asking about something unrelated to your scope, 
                hand off back to the agent you were transferred from.

        Available handoff tools:
        - `handoff_to_appointment_agent`

        Do not infer or reuse appointment or other intent-related information from previous message history or tool results. Treat each tool call independently and based only on the current message context.
      
      Handoff Rules:
      - When a user request contains multiple intents (e.g., "I want to see my order and my appointment"), identify which intent appears first in the user's message and handle that one first.
        add that as a ai message also.
      - If handling the intent requires a tool or a handoff to another agent:
          - Only call one tool or perform one handoff at a time.
          
          - Once a tool is called or a handoff is made, do not attempt to call another tool or initiate another handoff until the current one completes 
            and control is returned to you.

          - This is because only one node (agent) is active at a time in the swarm architecture. 
            Calling a second tool or agent during an active handoff will cause a conflict or be ignored.

        - If all requested actions in the query require handoff to other agents, handoff only once, based on the first mentioned intent, 
          and ignore the others until control is returned.
      
    """
    return [SystemMessage(content=system_prompt)] + state['messages']
  
  @staticmethod
  def create_agent():
    order_agent = create_react_agent(
      model=ChatOpenAI(model="gpt-4o-mini"),
      state_schema=MainState,
      tools=[get_order, transfer_to_idv_agent, transfer_to_appointment_agent],
      prompt=OrderAgent.agent_prompt,
      name=NodeName.order_agent.value
    )

    return order_agent
  
  @staticmethod
  def agent_prompt_for_supervisor(state: MainState):
    
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
        state_schema=MainState,
        prompt=OrderAgent.agent_prompt_for_supervisor,
        supervisor_name="order_agent_supervisor",
        output_mode="full_history"
    )
    
    return workflow.compile(name=NodeName.order_agent.value)