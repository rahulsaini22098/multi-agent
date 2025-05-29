from typing import Union
from verticals.provider.tools.handoff_tool_json import provider_handoff_tools_json
from verticals.provider.tools.tool_types import ProviderHandoffToolsJson

all_handoff_tools: Union[ProviderHandoffToolsJson]   = {
  **provider_handoff_tools_json
}