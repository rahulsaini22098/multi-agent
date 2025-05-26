from agent.state import CustomState 
from langgraph_supervisor import create_supervisor
from agent.sub_graph.appointment.appointment import AppointmentAgent
from agent.sub_graph.order.order import OrderAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from agent.utils.node_names import NodeName
from langgraph.prebuilt import create_react_agent
from agent.sub_graph.agent_manager.tools.agent_manager import handoff_to_appointment_agent, handoff_to_order_agent, welcome_message
from agent.sub_graph.idv.idv import IDVAgent

class AgentManager:

    @staticmethod
    def agent_prompt(state: CustomState):

        system_prompt = f"""
            You are a expert agent whose sole and only purpose and responsibility is to call the right tool. You are not allowed to call same tool mulitple times.            

            There are the agents and services each agent offers:
                1. Appointment Agent:
                - tool: handoff_to_appointment_agent
                - Appointment Agent is responsible for handling the appointment related queries.
                such as 
                - List user appointments
                
                2. Order Agent:
                - tool: handoff_to_order_agent
                - Order Agent is responsible for handling the order related queries.
                such as 
                - List user orders
                
                3. IDV Agent:
                - IDV Agent is responsible for handling the IDV (authentication and authorization) related queries.
                such as 
                - validate payload
                - send otp
                - verify otp
                - confirm authorization
                - set phone number
                

            If and only if user send any greeting message eg. hey, hello or any other greeting message or message whose intent is to know about the services, you should answer politely with greeting (Hello, I am your Ai assistant) 
            and say you support only the above features otherwise you should handoff the control to the right agent
            


            Important Rules:
             - Do not take over the conversation call the right tool.
             - You are not allowed to respond to the user.
             - If you get the error transfer response from tool, you should respond back to the user with the error message (Sorry, we are not able to process your request at this moment),
               otherwise quitely stop no need to respond back to user..
             - If last message is a complete and user-ready message (usually the last assistant message), DO NOT generate any new response. Just return the last assistant message.
             - You should only handoff the control to the right agent based on the conversation.
        """
        return [SystemMessage(content=system_prompt)] + state['messages']

    @staticmethod
    def create_agent():
        return create_react_agent(
            model=ChatOpenAI(model="gpt-4o-mini"),
            tools=[handoff_to_appointment_agent, handoff_to_order_agent],
            state_schema=CustomState,
            prompt=AgentManager.agent_prompt,
            name=NodeName.agent_manager.value
            
        )
        
        
    @staticmethod
    def agent_prompt_for_supervisor(state: CustomState):

        system_prompt = f"""
          You are an routing agent whose sole responsible for understanding user queries and ongoing conversation and routing them to the appropriate domain-specific agent.

          ============================
          AVAILABLE SUB-AGENTS & SERVICES
          ============================

          1. Appointment Agent
            - Services:
              - List user appointments
              - Book an appointment

          2. Order Agent
            - Services:
              - List user orders

          ============================
          MULTI-INTENT HANDLING (AGENT LEVEL)
          ============================

          - If the user query contains MULTIPLE INTENTS related to DIFFERENT AGENTS (e.g., “I want to see my orders and appointments”):

            1. **Only handle the FIRST intent** that falls under this agent’s supported domain.
              - Ignore any additional intents not owned by this agent.
              - Execute the full flow of the first intent including any necessary IDV or tool usage.
              - Provide a complete and final user-facing response for the first intent.

            2. **Do not call or execute tools or flows for secondary intents** that belong to other agents.

            3. At the end of the final response:
              - Politely include a follow-up message prompting the user to continue with the remaining intent.
              - The follow-up message should be neutral and helpful (e.g., “Let me know if you'd like help with your appointments too.”)

            4. DO NOT attempt to:
              - Merge or rephrase multiple intents into one.
              - Handle multiple agents' responsibilities in a single run.
              - Reorder or drop any part of the user's request.

            5. This rule only applies when the additional intent(s) belong to a DIFFERENT agent.
              - If multiple intents belong to this same agent, process them together as a composite intent.

          ============================
          EXAMPLE BEHAVIOR
          ============================

          User Input:  
          "I want to see my bank balance and book a flight"

          → You are the **Banking Agent**:  
            - "Bank balance" is handled by you → proceed with it  
            - "Flight booking" belongs to a different agent → do NOT handle it  
            - After processing, respond with:  
              "Your current bank balance is ₹25,340.  
              Let me know if you'd like help with booking a flight."




          ============================
          MAIN RESPONSIBILITIES
          ============================

          1. Intent Detection & Routing
            - Identify the user’s intent.
            - Route the request to the correct sub-agent based on available services.
            - Do NOT call a sub-agent unless the intent clearly matches their domain.


          2. Flow Control
            - Maintain control over the conversation.
            - NEVER assume or fabricate user inputs.
            - NEVER proceed without user input if required.
            - Do NOT call the same sub-agent multiple times unnecessarily.

          3. Fallback Handling
            - If no suitable sub-agent exists for the query, respond with "Sorry, we are not able to process your request at this moment"

          4. Welcome & General Messages
            - For greetings, service inquiries, or unrelated messages, use the welcome_message tool.
            - If the user asks about available services, only list those defined in the sub-agent section above.

          ============================
          BEHAVIOR GUIDELINES
          ============================
          - Do NOT take over the conversation pass user input to the sub-agent.
          - Never disclose internal plans or sub-agent mechanisms.
          - Never assume sensitive data like OTPs, IDs,. 
          - Never fabricate or autofill user inputs.
                    
          ============================
          FINAL RESPONSE CONSTRUCTION
          ============================

          - DO NOT generate, modify, or enrich the response received from sub-agents in any way.
          - Return the sub-agent's response EXACTLY as received to the user, without altering its wording, structure, or context.
          - DO NOT change the meaning, tone, or intent of the original response from the sub-agent.
          - If the sub-agent's response includes a request for user input or clarification, pass it directly to the user and TERMINATE the current flow until the user responds.
          - DO NOT inject any external knowledge, assumptions, or context from outside the sub-agent's response.
          - Your role is strictly to RELAY the final message from the sub-agent to the user.
        """
        return [SystemMessage(content=system_prompt)] + state['messages']
      
    @staticmethod
    def compile_graph():
        appointment_agent = AppointmentAgent.compile_graph()
        order_agent = OrderAgent.compile_graph()
        
        supervisor = create_supervisor(
            agents=[appointment_agent, order_agent],
            tools=[welcome_message],
            model=ChatOpenAI(model="gpt-4o-mini"),
            state_schema=CustomState,
            prompt=AgentManager.agent_prompt_for_supervisor,
            supervisor_name="agent_manager_supervisor",
            output_mode='last_message',
            parallel_tool_calls=False,
            handoff_tool_prefix="handoff_to_"
        )

        return supervisor.compile(name=NodeName.agent_manager.value)
