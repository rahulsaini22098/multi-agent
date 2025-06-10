from typing import Union
from verticals.provider.tools.tools_json import provider_tools_json
from verticals.provider.tools.tool_types import ProviderToolsJson
from verticals.retail.tools.tools_json import retail_tools_json
from verticals.retail.tools.tool_types import RetailToolsJson
from verticals.banking.tools_json import banking_tools_json
from verticals.banking.tool_types import BankingToolsJson

all_tools: Union[ProviderToolsJson, RetailToolsJson, BankingToolsJson] = {
  **provider_tools_json,
  **retail_tools_json,
  **banking_tools_json
}