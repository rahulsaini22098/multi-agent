from verticals.provider.tools import ProviderToolsJson, welcome_message, get_appointments

provider_tools_json: ProviderToolsJson = {
   "welcome_message": {
      "description": "welcome message to the customer",
      "tool": welcome_message
    },
   "get_appointments": {
      "description": "get all the appointments of the customer",
      "tool": get_appointments
    },
}

   