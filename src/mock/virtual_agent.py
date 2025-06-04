from typing import TypedDict, Dict, Any, List, Optional
from enum import Enum

class Vertical(Enum):
    PROVIDER = "provider"
    RETAIL = "retail"
    BANKING = "banking"

class VoiceChannelConfig(TypedDict):
    _id: Optional[Dict[str, str]]
    revision_id: Optional[str]
    created_at: Dict[str, Dict[str, str]]
    updated_at: Optional[Dict[str, Dict[str, str]]]
    voice: str
    tts_provider: str
    transcription_provider: str
    max_silence_seconds: int

class VirtualAgent(TypedDict):
    _id: Dict[str, str]
    created_at: Dict[str, Dict[str, str]]
    updated_at: Dict[str, Dict[str, str]]
    name: str
    description: Optional[str]
    virtual_agent_id: str
    account_id: str
    dialed_tn: str
    welcome_greeting: str
    configured_agent_ids: List[str]
    configured_channels: List[str]
    is_inform_flow_enabled: bool
    is_predictive_flow_enabled: bool
    is_next_best_action_flow_enabled: bool
    voice_channel_config: VoiceChannelConfig
    vertical: Vertical
    created_by: str
    updated_by: str

virtual_agent: VirtualAgent = {
    "_id": {
        "$oid": "6821f17afbe13c5e3903ccdb"
    },
    "created_at": {
        "$date": {
            "$numberLong": "1747054970262"
        }
    },
    "updated_at": {
        "$date": {
            "$numberLong": "1747205341931"
        }
    },
    "name": "Provider Virtual Agent",
    "description": None,
    "virtual_agent_id": "88963599-ea7a-44b2-be81-6df732c56194",
    "account_id": "test-account-1",
    "dialed_tn": "+18555032476",
    "welcome_greeting": "Welcome to Modern Clinic.",
    "configured_agent_ids": [
        "b558b61e-cc43-456e-aea8-cfde78e1cbf4",
        "c76e2f31-5a08-4e27-9c19-04d6b1c724a8"
    ],
    "configured_channels": ["voice"],
    "is_inform_flow_enabled": True,
    "is_predictive_flow_enabled": True,
    "is_next_best_action_flow_enabled": True,
    "voice_channel_config": {
        "_id": None,
        "revision_id": None,
        "created_at": {
            "$date": {
                "$numberLong": "1747054970262"
            }
        },
        "updated_at": None,
        "voice": "en-US-Journey-O",
        "tts_provider": "google",
        "transcription_provider": "deepgram",
        "max_silence_seconds": 10
    },
    "vertical": Vertical.PROVIDER,
    "created_by": "system",
    "updated_by": "system"
}