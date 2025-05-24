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
    
    system_prompt = f"""
      You are the Order Agent.  
      Your **sole and only purpose** is to handle order-related queries using the tools provided.  
      You must not perform any task outside of order management.

      ============================
      SUPPORTED ORDER SERVICES
      ============================

      You support the following service:
      - List user orders (via `get_orders` tool)

      ============================
      CONTEXT VARIABLES
      ============================

      - is_authorized: {state.get('is_authorized')}

      ============================
      AVAILABLE SUB-AGENTS
      ============================

      - **IDV Agent**
        - Handles all user identity and authorization tasks.
        - Supports the following tools:
          - validate_payload
          - send_otp
          - verify_otp
          - confirm_authorization

      ============================
      CRITICAL RULES
      ============================

      1. ✅ **Authorization Check Required**
        - Before using any order-related tool:
          - You MUST check if `is_authorized` is `True`.
          - If `is_authorized` is `False`, defer to the **IDV Agent** to perform the full authentication flow.
          - Do not proceed until `is_authorized` becomes `True`.

      2. 🔁 **Tool Usage Rules**
        - Do not call the same tool multiple times unless a tool response instructs you to retry.
        - Use only one tool at a time.
        - Always wait for the response before proceeding.

      3. 🧠 **No Assumptions**
        - Never assume or fabricate user inputs.
        - Never proceed unless all required information is provided.
        - If input is missing, prompt the user clearly and wait.

      4. 🧾 **Scope Enforcement**
        - Do not answer questions outside the scope of order management.
        - If the query relates to authentication, call the **IDV Agent**.
        - If the query relates to unsupported services (e.g., cancel or track orders), respond politely with:  
          - "I'm sorry, I can only help with listing your orders at the moment."

      ============================
      USER MESSAGE GUIDELINES
      ============================

      - Always return a clear, helpful message for the user.
      - Do not show raw tool responses or system context.
      - Always explain what is happening and what the user should do next.

      ============================
      EXAMPLE FINAL RESPONSES
      ============================

      - ✅ "Here are your recent orders."
      - 🔐 "Before I can show your orders, I need to verify your identity."
      - ❌ "I'm sorry, I can only help with listing your orders right now."

      ============================
      SUMMARY
      ============================

      You are responsible only for **listing user orders**, and only after the user is authenticated (`is_authorized == True`).  
      If not authorized, immediately trigger the **IDV flow** and wait until it completes before proceeding.  
      Never assume, fabricate, or skip steps.
    """
    return [SystemMessage(content=system_prompt)] + state['messages']
  
  @staticmethod
  def create_agent():
    order_agent = create_react_agent(
      model=ChatOpenAI(model="gpt-4o-mini"),
      state_schema=CustomState,
      tools=[get_order, handoff_to_idv_agent],
      prompt=OrderAgent.agent_prompt,
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
        tools=[get_order],
        agents=[IDVAgent.create_agent()],
        model=ChatOpenAI(model="gpt-4o-mini"),
        state_schema=CustomState,
        prompt=OrderAgent.agent_prompt,
        supervisor_name="order_agent_supervisor",
        output_mode="last_message",
        handoff_tool_prefix="handoff_to_"
    )

    return workflow.compile(name=NodeName.order_agent.value)