from verticals.provider.tools import ProviderToolsJson, welcome_message, get_appointments, book_appointment, confirm_appointment, cancel_appointment, create_appointment, reschedule_appointment, get_appointment_details, list_services

provider_tools_json: ProviderToolsJson = {
   "welcome_message": {
      "description": "This tool return the welcome message if user send any greeting message eg. hey, hello or any other greeting message or call the `welcome_message` tool.",
      "tool": welcome_message
    },
   "get_appointments": {
      "description": "get all the appointments of the customer",
      "tool": get_appointments
    },
   "book_appointment": {
      "description": "This tool is used to book an appointment for the customer. It requires data and time from the customer.",
      "tool": book_appointment
    },
   "confirm_appointment": {
      "description": "This tool is used to confirm an appointment for the customer. It requires appointment id from the customer.",
      "tool": confirm_appointment
    },
   "cancel_appointment": {
      "description": "This tool is used to cancel an appointment for the customer. It requires appointment id from the customer.",
      "tool": cancel_appointment
    },
   "create_appointment": {
      "description": "Create a new appointment for the customer.",
      "tool": create_appointment
    },
   "reschedule_appointment": {
      "description": "Reschedule an existing appointment for the customer.",
      "tool": reschedule_appointment
    },
   "get_appointment_details": {
      "description": "Get details of a specific appointment for the customer.",
      "tool": get_appointment_details
    },
   "list_services": {
      "description": "List all available services to the customer.",
      "tool": list_services
    }
}

   