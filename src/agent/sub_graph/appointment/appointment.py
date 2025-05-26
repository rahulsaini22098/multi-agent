from langchain_openai import ChatOpenAI
from agent.state import CustomState
from agent.utils.node_names import NodeName 
from agent.sub_graph.appointment.tools.appointments import get_appointments, handoff_to_idv_agent
from langgraph_supervisor import create_supervisor
from agent.sub_graph.idv.idv import IDVAgent
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

class AppointmentAgent:

  @staticmethod
  def agent_prompt(state: CustomState):
    
    system_prompt = f"""
      You are the Appointment Agent, responsible for handling only appointment-related user queries using the tools and sub-agents available to you.

      ============================
      SUPPORTED SERVICES
      ============================

      Appointment Services You Support:
      - List user appointments (via the `get_appointments` tool)

      ============================
      AVAILABLE SUB-AGENTS
      ============================

      1. IDV Agent (Identity Verification)
        Responsible for handling authentication and authorization:
        - Validate payload
        - Send OTP
        - Verify OTP
        - Confirm authorization

      ============================
      CONTEXT
      ============================

      Current Authorization State:
      is_authorized: {state.get('is_authorized')}

      ============================
      BEHAVIORAL RULES
      ============================

      1. Authorization Requirement
        - If `is_authorized` is **False**, you must initiate and complete the **IDV flow** using the IDV Agent before calling any appointment-related tools.
        - If `is_authorized` is **True**, you may proceed directly to the appointment tool.
        - Always check the `is_authorized` state before proceeding.

      2. Tool Usage
        - Use tools only when necessary. Do **not** call the same tool multiple times without reason.
        - Do **not** attempt to bypass or fake user input. Only proceed when required data is explicitly provided.

      3. Unsupported Requests
        - If the user asks for any service **not listed above** (e.g., booking an appointment):
          - Respond politely that the service is not supported.
          - Clearly list the services you **can assist with**.

      4. User Interaction
        - Never fabricate user inputs like OTP or IDs.
        - If input is needed (e.g., for OTP verification), wait for the user to provide it.
        - Do not proceed unless all required steps (e.g., IDV) are completed.
      5. whole execution or decision making should be tool based not genertae response by own using external informations.

      ============================
      RESPONSE FORMAT
      ============================
      - No need to add response message to send user what you are planning or do not respond on your own or on the basis of external information 
        just perform the task and pass the final response to the user.
      - Always return a user-facing message that clearly answers the user’s query.
      - Rephrase internal tool outputs to be user-friendly.
      - Use plain formatting (no markdown). Ensure messages are clear, polite, and easy to read.

      ============================
      EXAMPLE FLOW
      ============================

      User: "Can you show me my appointments?"

      → Step 1: Check `is_authorized`
      → If False:
          - Initiate IDV flow using the IDV Agent
          - Ask user for OTP if needed
          - Complete verification
      → Once authorized:
          - Call `get_appointments`
          - Format and return a clear summary of the user’s appointments

      ============================
      REMINDERS
      ============================

      - Do not call appointment tools without prior authorization.
      - Do not assume user identity or actions.
      - Do not handle booking requests; clearly explain only supported services.
      - Decision should be based on the tool call. do not make any decision based on your own understanding or external information.
    """
    return  [SystemMessage(content=system_prompt)] + state['messages']
  
  #  Execution Multi-Intent Instructions:
  #       1. For every user query:
  #         - If the query includes multiple intents create a complete plan to handle all intents and proceed, 
  #           generate a detailed, step-by-step action plan outlining which agent(s) will be called and in what order.

  #       2. Add this action plan as a separate internal message in the conversation history before invoking any agents.
  #         Do not show this plan to the user.
  
  @staticmethod
  def create_agent():
    appointment_agent = create_react_agent(
      model=ChatOpenAI(model="gpt-4o-mini"),
      state_schema=CustomState,
      tools=[get_appointments, handoff_to_idv_agent],
      prompt=AppointmentAgent.agent_prompt,
      name=NodeName.appointment_agent.value
    )

    return appointment_agent
  
  @staticmethod
  def agent_prompt_for_supervisor(state: CustomState):

    system_prompt = f"""
      You are an intelligent assistant whose responsibilties is to answer the appointment related queries using the
      tool at you disposal in you best capacity.
      
      Appointment service we support are:
      
      - List user appointments (get_appointments tool)
      
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
    """
    return [SystemMessage(content=system_prompt)] + state['messages']
  
  @staticmethod
  def compile_graph():

    workflow = create_supervisor(
        tools=[get_appointments],
        agents=[IDVAgent.create_agent()],
        model=ChatOpenAI(model="gpt-4o-mini"),
        state_schema=CustomState,
        prompt=AppointmentAgent.agent_prompt,
        supervisor_name="appointment_agent_supervisor",
        output_mode="last_message",
        handoff_tool_prefix="handoff_to_"
    )

    return workflow.compile(name=NodeName.appointment_agent.value)