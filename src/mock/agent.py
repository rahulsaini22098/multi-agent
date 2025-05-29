from typing import TypedDict, Dict, Any, List

class AgentConfig(TypedDict):
    agent_id: str
    account_id: str
    display_name: str
    description: str
    instruction_provided: str
    agent_status: str
    agent_source: str
    configured_state_schema: Dict[str, Any]
    configured_tools: List[str]
    configured_system_prompt: str
    configured_completion_marker: str
    created_by: str
    updated_by: str
    created_at: Dict[str, Any]
    updated_at: Dict[str, Any]
    __v: int

agent_config: AgentConfig = {
  "_id": {
    "$oid": "6835b25cbc4d1772725d5c32"
  },
  "agent_id": "b558b61e-cc43-456e-aea8-cfde78e1cbf4",
  "account_id": "test-account-1",
  "display_name": "Provider AGent",
  "description": "A healthcare provider search assistant that helps patients find doctors based on specialty, location, or name. It supports filtering by city, zip code, or distance. The assistant can also check appointment availability with selected providers.",
  "instruction_provided": "Create a healthcare provider search assistant that helps patients find the right doctors for their needs. The assistant should:\n\n1. Help patients locate doctors and specialists based on medical specialty requirements\n2. Find providers based on location preferences (city, zip code, distance)\n3. Allow patients to search for specific doctors by name when preferred\n4. Check appointment availability for selected providers\n\n",
  "agent_status": "published",
  "agent_source": "user",
  "configured_state_schema": {
    "specialty": {
      "type": "string",
      "description": "The medical specialty the patient is looking for (e.g., Cardiology, Orthopedics)."
    },
    "location_type": {
      "type": "string",
      "description": "The type of location to search for (e.g., Clinic, Hospital)."
    },
    "city": {
      "type": "string",
      "description": "The city to search for healthcare providers."
    },
    "zip_code": {
      "type": "string",
      "description": "The zip code to filter healthcare providers."
    },
    "doctor_name": {
      "type": "string",
      "description": "The specific doctor's name the patient wants to search for."
    },
    "provider_id": {
      "type": "string",
      "description": "The ID of the selected provider to check appointment availability."
    },
    "available_appointment_date": {
      "type": "string",
      "description": "The date for which the patient wants to check appointment availability."
    },
    "distance": {
      "type": "number",
      "description": "The distance within which to search for providers."
    }
  },
  "configured_tools": [
    "get_appointments",
  ],
  "configured_system_prompt": "OBJECTIVE: Assist patients in finding the right healthcare providers based on their medical specialty requirements, location preferences, and specific doctor names, while also checking appointment availability.\n\nPROCESS: First, ask the patient for their desired medical specialty. Then, inquire about their location preferences, including city, zip code, and possibly distance. After collecting this information, if the patient has a specific doctor in mind, ask for the doctor's name. Once you have gathered all the relevant information, utilize the 'find_care_tool' to locate potential providers. After presenting the options, if the patient selects a provider, ask for the date they wish to check for appointment availability and use the 'get_appointments_tool' to find available slots for the selected provider.\n\nCONCLUSION: When you have collected all necessary information, provide a list of matching healthcare providers and their details. If the patient selects a provider, check and communicate the appointment availability for their chosen date.\n\nGENERAL_GUIDANCE: Retain all collected information throughout the conversation to ensure a smooth flow and do not ask for the same information again.",
  "configured_completion_marker": "FLOW_COMPLETE",
  "created_by": "1",
  "updated_by": "1",
  "created_at": {
    "$date": {
      "$numberLong": "1748349532618"
    }
  },
  "updated_at": {
    "$date": {
      "$numberLong": "1748350340688"
    }
  },
  "__v": 0
}