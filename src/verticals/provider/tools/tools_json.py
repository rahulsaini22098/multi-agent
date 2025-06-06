from verticals.provider.tools import ProviderToolsJson, welcome_message, get_appointments, book_appointment, confirm_appointment, cancel_appointment

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
    }
}

   