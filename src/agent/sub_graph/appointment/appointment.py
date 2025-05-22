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

    if state.get('is_authorized') is None or state.get('is_authorized') == False:
      system_prompt = f"""
      Its look like user is not authorized to for appointments services.
      call the handoff_to_idv_agent tool initiate the authroization flow so user can manage appointments.
      """
    
    else:
      system_prompt = f"""
      You are an expert agent who's sole and only purpose and responsibility is to handle the appointment related queries.

      These are the the feature you currently support:
      1. List user appointments

      If user asks about anything else, you should politely decline and say you support only the above features.

      You should only continue with the listed features if user is already authorised.

      Always make sure the last message should be the well structured ai response what can we shouw to user.
      Do not disclose and sensative information to user.
      
      Do not make the tool call in parallel. It should always be in sequence.
    """

    return  [SystemMessage(content=system_prompt)] + state['messages']
  
  @staticmethod
  def create_agent():
    appointment_agent = create_react_agent(
      model=ChatOpenAI(model="gpt-4o-mini"),
      state_schema=CustomState,
      tools=[get_appointments],
      prompt=AppointmentAgent.agent_prompt_for_supervisor,
      name=NodeName.appointment_agent.value
    )

    return appointment_agent
  
  @staticmethod
  def agent_prompt_for_supervisor(state: CustomState):

    if state.get('is_authorized') is None or state.get('is_authorized') == False:
      system_prompt = f"""
      Its look like user is not authorized to for appointments related queries. supervisor need to handoff the control to idv agent to authenticate the user first.
      
      Do not make any tool call related to appointments.
      """
    
    else:
      system_prompt = f"""
      You are an expert agent who's sole and only purpose and responsibility is to handle the appointment related queries.

      These are the the feature you currently support:
      1. List user appointments

      If user asks about anything else, you should politely decline and say you support only the above features.

      You should only continue with the listed features if user is already authorised.

      Always make sure the last message should be the well structured ai response what can we shouw to user.
      Do not disclose and sensative information to user.
      
      Do not make the tool call in parallel. It should always be in sequence.
    """

    return  [SystemMessage(content=system_prompt)] + state['messages']
  


  @staticmethod
  def compile_graph():

    workflow = create_supervisor(
        tools=[get_appointments],
        agents=[IDVAgent.create_agent()],
        model=ChatOpenAI(model="gpt-4o-mini"),
        state_schema=CustomState,
        prompt=AppointmentAgent.agent_prompt_for_supervisor,
        supervisor_name="appointment_agent_supervisor",
        output_mode="full_history"
    )

    return workflow.compile(name=NodeName.appointment_agent.value)