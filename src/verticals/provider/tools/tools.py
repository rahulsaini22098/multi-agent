from typing import Annotated
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
import json
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId
from agent.state import MainState
from langchain_core.tools import tool
from mock.provider import providerStore, Appointment, AppointmentStatus
import uuid
from utils.datetime import get_current_datetime_in_ist
from .tool_types import BOOK_APPOINTMENT, CONFIRM_APPOINTMENT, CANCEL_APPOINTMENT, RESCHEDULE_APPOINTMENT, GET_APPOINTMENTS, WELCOME_MESSAGE, CREATE_APPOINTMENT, GET_APPOINTMENT_DETAILS, LIST_SERVICES


@tool(
   WELCOME_MESSAGE,
   description="""
   It is used to send the welcome message to the user.
   """)
def welcome_message(
   state: Annotated[MainState, InjectedState], 
   tool_call_id: Annotated[str, InjectedToolCallId]
):
   welcome_message = state["welcome_message"] or "Hello, I am your Ai assistant. I can help you with your appointment and order related queries."
   tool_message = ToolMessage(content=welcome_message, tool_call_id=tool_call_id)
   
   return Command(update={"messages": state['messages'] + [tool_message]})
 
 
@tool(GET_APPOINTMENTS, 
      description="""It is used to get all the appointments of the customer"""
)
def get_appointments(
  state: Annotated[MainState, InjectedState], 
  tool_call_id: Annotated[str, InjectedToolCallId]
):   
  print(f"Looking up appointment for customer {state['customer_id']}")
  customer_id = state['customer_id']
  
  if customer_id is None or customer_id == "":
    return Command(
        update={
          "messages": state['messages'] + [
              ToolMessage(content="Customer ID is required to get appointments", tool_call_id=tool_call_id)
          ]
        }
    )
  
  
  appointments = providerStore.get_appointments(customer_id=customer_id)
  
  return Command(
    update={
      "messages": state['messages'] + [
        ToolMessage(content=f"Here are the appointments: {json.dumps(appointments)}", tool_call_id=tool_call_id)
      ]
    }
  ) 


@tool(BOOK_APPOINTMENT,
  description=f"""
  Books an appointment for the customer using a valid date and time.
  
  Input Requirements:
    - Date: Must be in MM-DD-YYYY format.
    - Time: Must be in HH:MM (24-hour format).

  Parsing Rules:
    - Interpret all relative date/time expressions (e.g., "next Sunday", "tomorrow") using the current date and time ({get_current_datetime_in_ist()}) 
      in IST as per user's timezone (India Standard Time).
    - Always resolve to the correct current year (e.g., if today is June 6, 2025, "next Sunday" is June 8, 2025).
    - Time must also be valid according to IST timezone.

  """)
def book_appointment(
  date: str,
  time: str,
  state: Annotated[MainState, InjectedState], 
  tool_call_id: Annotated[str, InjectedToolCallId]
):
 
  print(f"Booking appointment for customer {state['customer_id']}")
  customer_id = state['customer_id']
  
  if customer_id is None or customer_id == "":
    return Command(
        update={
          "messages": state['messages'] + [
              ToolMessage(content="Customer ID is required to book appointment", tool_call_id=tool_call_id)
          ]
        }
    )
    
  appointment = Appointment(
    id=str(uuid.uuid4()),
    customer_id=customer_id,
    date=date,
    time=time,
    status=AppointmentStatus.PENDING,
    
  )
    
  providerStore.add_appointment(appointment=appointment)
  
  return Command(
    update={
      "messages": state['messages'] + [
        ToolMessage(content=f"Appointment booked successfully for {date} at {time}", tool_call_id=tool_call_id)
      ]
    }
  )
  
@tool(CONFIRM_APPOINTMENT,
  description=f"""
  Confirms an appointment for the customer using a valid appointment id.
  
  Input Requirements:
    - Appointment ID: Must be a valid appointment id.
    
  Parsing Rules:
    - Appointment ID must be a valid appointment id.
  """)
def confirm_appointment(
  appointment_id: str,
  state: Annotated[MainState, InjectedState], 
  tool_call_id: Annotated[str, InjectedToolCallId]
):
  print(f"Confirming appointment for customer {state['customer_id']}")
  customer_id = state['customer_id']
  
  if customer_id is None or customer_id == "":
    return Command(
        update={
          "messages": state['messages'] + [
              ToolMessage(content="Customer ID is required to confirm appointment", tool_call_id=tool_call_id)
            ]
        }
    )
  
  appointment = providerStore.get_appointment(appointment_id=appointment_id)
  
  if appointment is None:
    return Command(
        update={
          "messages": state['messages'] + [ ToolMessage(content=f"Appointment {appointment_id} not found", tool_call_id=tool_call_id) ]
        }
    )
    
  if appointment.status == AppointmentStatus.CONFIRMED:
    return Command(
        update={
          "messages": state['messages'] + [ ToolMessage(content=f"Appointment {appointment_id} is already confirmed", tool_call_id=tool_call_id) ]
        }
    )
  
  if appointment.status == AppointmentStatus.COMPLETED:
    return Command(
        update={
          "messages": state['messages'] + [ ToolMessage(content=f"Appointment {appointment_id} is already completed", tool_call_id=tool_call_id) ]
        }
    )
    
  providerStore.update_appointment(appointment_id=appointment_id, status=AppointmentStatus.CONFIRMED)
  
  return Command(
    update={
      "messages": state['messages'] + [ ToolMessage(content=f"Appointment {appointment_id} confirmed successfully", tool_call_id=tool_call_id) ]
    }
  )
  
@tool(CANCEL_APPOINTMENT,
  description=f"""
  Cancels an appointment for the customer using a valid appointment id.
  
  Input Requirements:
    - Appointment ID: Must be a valid appointment id.
    
  Parsing Rules:
    - Appointment ID must be a valid appointment id.
  """)
def cancel_appointment(
  appointment_id: str,
  state: Annotated[MainState, InjectedState], 
  tool_call_id: Annotated[str, InjectedToolCallId]
):
  print(f"Cancelling appointment for customer {state['customer_id']}")
  customer_id = state['customer_id']
  
  if customer_id is None or customer_id == "":
    return Command(
        update={
          "messages": state['messages'] + [ ToolMessage(content="Customer ID is required to cancel appointment", tool_call_id=tool_call_id) ]
        }
    )
  
  appointment = providerStore.get_appointment(appointment_id=appointment_id)
  
  if appointment is None:
    return Command(
        update={
          "messages": state['messages'] + [ ToolMessage(content=f"Appointment {appointment_id} not found", tool_call_id=tool_call_id) ]
        }
    )
  
  if appointment.status == AppointmentStatus.COMPLETED:
    return Command(
        update={
          "messages": state['messages'] + [ ToolMessage(content=f"Appointment {appointment_id} is already completed, cannot be cancelled", tool_call_id=tool_call_id) ]  
        }
    )
  
  providerStore.update_appointment(appointment_id=appointment_id, status=AppointmentStatus.CANCELLED)
  
  return Command(
    update={
      "messages": state['messages'] + [ ToolMessage(content=f"Appointment {appointment_id} cancelled successfully", tool_call_id=tool_call_id) ]
    }
  )
""" Define stub implementation for create_appointment """
@tool(CREATE_APPOINTMENT, description="Create a new appointment for the customer.")
def create_appointment(state: Annotated[MainState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    tool_message = ToolMessage(content="Appointment created successfully.", tool_call_id=tool_call_id)
    return Command(update={"messages": state['messages'] + [tool_message]})

""" Define stub implementation for reschedule_appointment """
@tool(RESCHEDULE_APPOINTMENT, description="Reschedule an existing appointment for the customer.")
def reschedule_appointment(state: Annotated[MainState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    tool_message = ToolMessage(content="Appointment rescheduled successfully.", tool_call_id=tool_call_id)
    return Command(update={"messages": state['messages'] + [tool_message]})

""" Define stub implementation for get_appointment_details """
@tool(GET_APPOINTMENT_DETAILS, description="Get details of a specific appointment for the customer.")
def get_appointment_details(state: Annotated[MainState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    details = json.dumps({"appointment_id": "sample-id", "date": "2024-01-01", "time": "10:00 AM"})
    tool_message = ToolMessage(content=details, tool_call_id=tool_call_id)
    return Command(update={"messages": state['messages'] + [tool_message]})

""" Define stub implementation for list_services """
@tool(LIST_SERVICES, description="List all available services to the customer.")
def list_services(state: Annotated[MainState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    services = json.dumps(["Consultation", "Checkup", "Therapy"])
    tool_message = ToolMessage(content=services, tool_call_id=tool_call_id)
    return Command(update={"messages": state['messages'] + [tool_message]})