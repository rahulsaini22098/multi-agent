from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from agent.state import CustomState
from agent.utils.node_names import NodeName
from agent.sub_graph.idv.tools.idv import send_otp, verify_otp, confirm_authorization, handoff_to_appointment_agent, set_phone_number, validate_payload, handoff_to_order_agent
class IDVAgent:
    @staticmethod
    def agent_prompt(state: CustomState) -> str:
        # Include user_provided_otp in the prompt if it exists
        
        system_prompt = f"""
            You are an identity verification (IDV) agent responsible for validating users before they access other services.

            Your goals:
            - Verify the user's identity by asking for OTP or confirming validation steps.
            - Use the provided tools to send OTP, validate OTP, and confirm authorization.
            - Before setting the phone number, always call the 'validate_payload' tool to check if the phone number is present and valid.
            - If 'validate_payload' returns a message saying "Phone number is required", prompt the user politely to provide their phone number.
            - When the user provides a valid phone number, call the 'set_phone_number' tool to save it in state.
            - Only proceed to send OTP after the phone number is successfully set.
            - If the user is successfully authorized (state key 'is_authorized' is true), immediately transfer the conversation to the next appropriate agent using the handoff tool.
            - If the user is not authorized yet, guide them clearly on the steps to verify their identity.
            - Always provide clear, concise, and polite messages.
            - Do NOT reveal internal system details or raw tool responses to the user.
            - If the user inputs invalid information (e.g., wrong OTP), prompt them to try again.
            - If a handoff is initiated, do NOT continue the conversation; stop and trigger handoff.
            - Use the tools responsibly and only when necessary.

            Remember, your ultimate goal is to securely verify the user and then transfer control smoothly to the next agent.
            Always make sure IF you send any message to the user, the last message should be a well-structured AI response suitable for display.


         """

        return [SystemMessage(content=system_prompt)] + state['messages']

    @staticmethod
    def create_agent():
        # transfer_to_appointment_agent = Utils.create_handoff_tool(agent_name=NodeName.appointment_agent.value, description="Transfer to appointment agent")
        # transfer_to_order_agent = Utils.create_handoff_tool(agent_name=NodeName.order_agent.value, description="Transfer to order agent")
        
        return create_react_agent(
            model=ChatOpenAI(model="gpt-4o-mini"),
            tools=[
                set_phone_number,
                send_otp,
                verify_otp,
                confirm_authorization,
                validate_payload,
                # handoff_to_order_agent,
                # handoff_to_appointment_agent,
                # add_human_in_the_loop(IDVAgent.verify_otp),
            ],
            state_schema=CustomState,
            name=NodeName.idv_agent.value,
            prompt=IDVAgent.agent_prompt,
        )