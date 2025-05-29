from typing import Union
from verticals.provider.tools.tools_json import provider_tools_json
from verticals.provider.tools.tool_types import ProviderToolsJson

all_tools: Union[ProviderToolsJson] = {
  **provider_tools_json
}