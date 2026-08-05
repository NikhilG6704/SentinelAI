"""
Monitoring Agent Schemas.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class AgentStatus(str, Enum):
    ONLINE = "Online"
    OFFLINE = "Offline"


class MonitoringAgentCreate(BaseModel):

    infrastructure_asset_id: int

    agent_name: str

    agent_version: str


class MonitoringAgentUpdate(BaseModel):

    agent_version: str | None = None

    status: AgentStatus | None = None

    last_heartbeat: datetime | None = None


class MonitoringAgentResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int

    infrastructure_asset_id: int

    agent_name: str

    agent_version: str

    registration_token: str

    last_heartbeat: datetime

    status: AgentStatus

    created_at: datetime

    updated_at: datetime