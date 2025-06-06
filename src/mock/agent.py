from typing import TypedDict, Dict, Any, List
from enum import Enum
from verticals import Vertical

class AgentConfig(TypedDict):
    agent_id: str
    account_id: str
    display_name: str
    description: str
    vertical: Vertical
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
    needs_verification: bool
    __v: int

provider_agent: AgentConfig = {
  "_id": {
    "$oid": "6835b25cbc4d1772725d5c32"
  },
  "agent_id": "b558b61e-cc43-456e-aea8-cfde78e1cbf4",
  "account_id": "test-account-1",
  "display_name": "Provider AGent",
  "description": "A healthcare provider search assistant that helps patients find doctors based on specialty, location, or name. It supports filtering by city, zip code, or distance. The assistant can also check appointment availability with selected providers.",
  "vertical": Vertical.PROVIDER.value,
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
    "book_appointment",
    "reschedule_appointment",
    "cancel_appointment",
    "confirm_appointment",
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
  "needs_verification": True,
  "__v": 0
}

retail_agent: AgentConfig = {
  "_id": {
    "$oid": "6821f179fbe13c5e3903ccd0"
  },
  "created_at": {
    "$date": {
      "$numberLong": "1747054969480"
    }
  },
  "updated_at": None,
  "agent_id": "c76e2f31-5a08-4e27-9c19-04d6b1c724a8",
  "account_id": "test-account-1",
  "display_name": "Retail Agent",
  "description": "Manages customer order information with tracking, payment verification, and item-specific status updates throughout the fulfillment process",
  "vertical": Vertical.RETAIL.value,
  "instruction_provided": "Create a retail order management assistant that helps customers track and manage their purchases. The assistant should:\n\n1. Always load retail data first before accessing any order information\n2. Proactively identify order IDs, purchase dates, or zip codes from customer messages\n3. Help customers look up order status and tracking information\n4. Allow customers to check details of specific items within their orders\n5. Answer questions about payment processing and billing for orders\n6. End conversations with a completion marker when all order inquiries are addressed\n\nThe agent should maintain state information including order identifiers, order status, and payment details. Required tools should include retail data loading, order finding, status checking, payment detail retrieval, and item-specific lookup. The assistant should be extremely proactive in identifying order-related information from customer messages and immediately use that information to retrieve relevant order details.",
  "agent_status": "published",
  "agent_source": "user",
  "configured_state_schema": {
    "properties": {
      "order_id": {
        "type": [
          "string",
          "null"
        ],
        "description": "Order ID that was found"
      },
      "order_status": {
        "type": [
          "string",
          "null"
        ],
        "description": "Current status of the order"
      },
      "payment_details": {
        "type": [
          "string",
          "null"
        ],
        "description": "Payment details for the order"
      }
    }
  },
  "configured_tools": [
    "get_orders"
  ],
  "configured_system_prompt": "You are an extremely helpful and proactive customer service assistant for order management. Your goal is to help customers check their order status, track shipments, view order details, and resolve payment issues.\nPROCESS:\n1. FIRST STEP: **Always call `load_retail_data_tool` first** before attempting to search for any orders.\n2. ANALYZE LAST MESSAGE: Look *VERY CAREFULLY* at the MOST RECENT user message. Does it contain a potential Order ID, purchase date, or zip code? \n3. GET ORDER: If ANY user message has order details (ID, date, zip), IMMEDIATELY call `find_order_tool` with that information. \n4. GET ORDER STATUS: Once an order is found, check its status using `get_order_status_tool`.\n5. VIEW ORDER ITEMS: If the customer asks about specific items, use `find_item_in_order_tool` to get details.\n6. CHECK PAYMENT: If the customer has payment questions, use `get_order_payment_details_tool` to retrieve payment information.\n7. FINALIZE: Once you've provided the customer with all requested information, confirm if they need anything else and end with 'FLOW_COMPLETE' when the conversation is resolved.\nTOOL USAGE RULES:\n- ALWAYS call `load_retail_data_tool` at the start of a conversation before using other tools.\n- Be PROACTIVE. Use tools *immediately* if the user provides relevant info.\n- If any tool fails, inform the user clearly and ask specifically for the missing/correct info.\n- Prioritize using information from the *very last user message* to decide your next action or tool call.",
  "configured_completion_marker": "FLOW_COMPLETE",
  "created_by": "Placeholder: User/system identifier of creator",
  "updated_by": "Placeholder: User/system identifier of last updater",
  "needs_verification": True
}

agents: List[AgentConfig] = [
  provider_agent,
  retail_agent,
]