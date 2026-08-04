from enum import Enum


class AssetType(str, Enum):
    SERVER = "Server"
    VM = "VM"
    DOCKER_HOST = "Docker Host"


class EnvironmentType(str, Enum):
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"


class AssetStatus(str, Enum):
    HEALTHY = "Healthy"
    WARNING = "Warning"
    CRITICAL = "Critical"
    OFFLINE = "Offline"