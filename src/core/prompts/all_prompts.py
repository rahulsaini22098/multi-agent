from verticals import Vertical
from verticals.provider.prompts.prompts import agent_prompt as provider_agent_prompt
from verticals.retail.prompts.prompts import agent_prompt as retail_agent_prompt
from verticals.banking.prompts import agent_prompt as banking_agent_prompt

all_prompts = {
  Vertical.PROVIDER.value: provider_agent_prompt,
  Vertical.RETAIL.value: retail_agent_prompt,
  Vertical.BANKING.value: banking_agent_prompt,
}

