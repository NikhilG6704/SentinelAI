from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DashboardOverview(BaseModel):
    total_assets: int
    total_agents: int
    online_agents: int
    offline_agents: int
    total_metrics: int
    healthy_assets: int
    warning_assets: int
    critical_assets: int


class DashboardHealth(BaseModel):
    average_cpu_usage: float
    average_memory_usage: float
    average_disk_usage: float
    average_network_usage: float
    health_score: float


class AgentSummary(BaseModel):
    agent_id: int
    hostname: str
    latest_cpu: float
    latest_memory: float
    latest_disk: float
    status: str
    last_heartbeat: datetime | None

    model_config = ConfigDict(from_attributes=True)