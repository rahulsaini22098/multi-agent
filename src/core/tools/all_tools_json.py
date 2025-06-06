from typing import Union
from verticals.provider.tools.tools_json import provider_tools_json
from verticals.provider.tools.tool_types import ProviderToolsJson
from verticals.retail.tools.tools_json import retail_tools_json
from verticals.retail.tools.tool_types import RetailToolsJson

all_tools: Union[ProviderToolsJson, RetailToolsJson] = {
  **provider_tools_json,
  **retail_tools_json
}