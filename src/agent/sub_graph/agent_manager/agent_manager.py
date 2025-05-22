from agent.state import CustomState 
from langgraph_supervisor import create_supervisor
from agent.sub_graph.appointment.appointment import AppointmentAgent
from agent.sub_graph.order.order import OrderAgent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from agent.utils.node_names import NodeName
from langgraph.prebuilt import create_react_agent
from agent.sub_graph.agent_manager.tools.agent_manager import handoff_to_appointment_agent, handoff_to_order_agent
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
            You are a expert agent whose sole and only purpose and responsibility is to call the right agent.
            If you get any query in which you need to call the multiple agent do that in sequentila order until the flow of one agent is not completed do not execute the other agent.
            
            for exmaple user input `i want to see my order and appointment`
            the first order agent if user is not authorized you need to handoff the control to idv agent.
            then if any input is rerequired from user you respond back to user. do not run the appointment agent untill the flow of order agent is not completed.

            There are the agents and services each agent offers:
                1. Appointment Agent:
                - tool: handoff_to_appointment_agent
                - Appointment Agent is responsible for handling the appointment related queries.
                - For some of the appopintment agent services to access user need to authenticate hinmself first. SO when appointment agent return user is not authorized you need to run the idv agent.
                such as 
                - List user appointments
                
                2. Order Agent:
                - tool: handoff_to_order_agent
                - Order Agent is responsible for handling the order related queries.
                - For some of the order agent services to access user need to authenticate hinmself first. SO when order agent return user is not authorized you need to run the idv agent.
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
             - If last message is a complete and user-ready message (usually the last assistant message), DO NOT generate any new response. Just return the last assistant message.
             - You should only handoff the control to the right agent based on the conversation.
             - If a sub-agent has already replied with a complete and user-ready message (usually the last assistant message), DO NOT generate any new response. Just return the last assistant message.
        """
        return [SystemMessage(content=system_prompt)] + state['messages']


    @staticmethod
    def compile_graph():
        appointment_agent = AppointmentAgent.create_agent()
        order_agent = OrderAgent.create_agent()
        idv_agent = IDVAgent.create_agent()
        
        supervisor = create_supervisor(
            agents=[appointment_agent, order_agent, idv_agent],
            model=ChatOpenAI(model="gpt-4o-mini"),
            state_schema=CustomState,
            prompt=AgentManager.agent_prompt_for_supervisor,
            supervisor_name="agent_manager_supervisor",
            output_mode='last_message',
            parallel_tool_calls=False
            
        )

        return supervisor.compile(name=NodeName.agent_manager.value)
