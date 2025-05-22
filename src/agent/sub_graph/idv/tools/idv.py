from typing import Annotated
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain_core.messages import ToolMessage, AIMessage
from agent.state import CustomState
from langchain_core.tools import tool
from langchain_core.tools import InjectedToolCallId
from typing import Literal
from agent.utils.node_names import NodeName
# Store OTPs in memory (in production, use a proper database/cache)
MOCK_OTP = "123456"

@tool("handoff_to_appointment_agent", description="Transfer to appointment agent")
def handoff_to_appointment_agent(
    state: Annotated[CustomState, InjectedState], 
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command[Literal["appointment_agent"]]:
    cleaned = [m for m in state['messages'] if m.type != "system"]
    tool_message = ToolMessage(content="transfer to appointment agent", tool_call_id=tool_call_id)
    cleaned.append(tool_message)
    
    return Command(
        goto=NodeName.appointment_agent.value,
        graph=Command.PARENT,
        update={
            "is_authorized": state.get('is_authorized', False),
            "customer_id": state.get('customer_id', None),
            "messages": cleaned
        }
    )

@tool('handoff_to_order_agent', description="Transfer to order agent")
def handoff_to_order_agent(
    state: Annotated[CustomState, InjectedState], 
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command[Literal["order_agent"]]:
    cleaned = [m for m in state['messages'] if m.type != "system"]
    tool_message = ToolMessage(content="transfer to order agent", tool_call_id=tool_call_id)
    cleaned.append(tool_message)

@tool('set_phone_number', description="Set the phone number in the state if validate_payload tool ask for it")
def set_phone_number(phone_number: str, state: Annotated[CustomState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    tool_message = ToolMessage(content=f"Phone number set to {phone_number}", tool_call_id=tool_call_id)
    
    return Command(
        update={
            "phone_number": phone_number,
            "messages": state['messages'] + [tool_message]
        }
    )

@tool('validate_payload', description="Validate the payload before sending the otp")
def validate_payload(state: Annotated[CustomState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    
    message = 'payload validated successfully'
    if state['phone_number'] is None or state['phone_number'].strip() == "":
        message = "Phone number is required"
    
    tool_message = ToolMessage(content=message, tool_call_id=tool_call_id)
    
    return Command(
        update={
            "messages": state['messages'] + [tool_message]
        }
    )

@tool("send_otp", description="Send an OTP to the user's phone number")
def send_otp(state: Annotated[CustomState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    try:
        phone_number = state['phone_number']
        # In a real implementation, this would actually send an SMS
        print(f"Sending OTP: {MOCK_OTP} to phone number: {phone_number}")
        
        msg_list = list(state['messages'])
        msg_list.append(ToolMessage(
            name="send_otp",
            content=f"OTP sent successfully to {phone_number}",
            tool_call_id=tool_call_id
        ))

        msg_list.append(AIMessage(content=f"OTP sent successfully to {phone_number}"))

        return Command(
            update={
                "messages": msg_list,
                "otp_sent": True
            },
        )
    
    except Exception as e:
        return Command(
            update={
                "messages": [f"Failed to send OTP: {str(e)}"],
                "otp_sent": False
            },
        )

@tool("verify_otp", description="Verify the OTP for a given phone number")
def verify_otp(otp: str, state: Annotated[CustomState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    try:
        stored_otp = MOCK_OTP
        
        if not stored_otp:
            tool_message = ToolMessage(content="No OTP found for this phone number", tool_call_id=tool_call_id)
            return Command(
                update={
                    "messages": [tool_message]
                }
            )
        
        if stored_otp == otp:
            msg_list = list(state['messages'])
            msg_list.append(ToolMessage(
                name="verify_otp",
                content=f"OTP verified successfully",
                tool_call_id=tool_call_id
            ))

            return Command(
                update={ 
                    "customer_id": '101', 
                    "is_authorized": True,
                    "messages": msg_list
                },
            )
        
        tool_message = ToolMessage(content="Invalid OTP, Please enter the correct OTP", tool_call_id=tool_call_id)
        
        return Command(
            update={
                "messages": [tool_message]
            }
        )
    
    except Exception as e:
        tool_message = ToolMessage(content=f"OTP verification failed: {str(e)}", tool_call_id=tool_call_id)
        
        return Command(
            update={
                "messages": [tool_message]
            }
        )

@tool("confirm_authorization", description="Confirm the authorization of the user")
def confirm_authorization(state: Annotated[CustomState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    if state['is_authorized'] is True:
      return Command(
          update={
              "messages": state['messages'] + [ToolMessage(content="Authorization confirmed", tool_call_id=tool_call_id)]
          }
      )
    else:
      return Command(
          update={
              "messages": state['messages'] + [ToolMessage(content="User is not authorized", tool_call_id=tool_call_id)]
          }
      )
