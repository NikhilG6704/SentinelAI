from __future__ import annotations

"""
Application-wide constants for the SentinelAI AI Engine.
"""

# ==========================================================
# API Endpoints
# ==========================================================

INFRASTRUCTURE_ASSETS_ENDPOINT = "/infrastructure-assets"
MONITORING_AGENTS_ENDPOINT = "/monitoring-agents"
SYSTEM_METRICS_ENDPOINT = "/system-metrics"
ALERTS_ENDPOINT = "/alerts"
INCIDENTS_ENDPOINT = "/incidents"
SYSTEM_LOGS_ENDPOINT = "/system-logs"
RECOVERY_WORKFLOWS_ENDPOINT = "/recovery-workflows"
AUDIT_LOGS_ENDPOINT = "/audit-logs"

# ==========================================================
# Timestamp Columns
# ==========================================================

CREATED_AT = "created_at"
UPDATED_AT = "updated_at"

COLLECTION_TIMESTAMP = "collection_timestamp"
TRIGGERED_AT = "triggered_at"
DETECTED_AT = "detected_at"
LOG_TIMESTAMP = "log_timestamp"
LAST_HEARTBEAT = "last_heartbeat"
STARTED_AT = "started_at"
COMPLETED_AT = "completed_at"
PERFORMED_AT = "performed_at"

TIMESTAMP_COLUMNS = [
    CREATED_AT,
    UPDATED_AT,
    COLLECTION_TIMESTAMP,
    TRIGGERED_AT,
    DETECTED_AT,
    LOG_TIMESTAMP,
    LAST_HEARTBEAT,
    STARTED_AT,
    COMPLETED_AT,
    PERFORMED_AT,
]

# ==========================================================
# Supported Scalers
# ==========================================================

STANDARD_SCALER = "standard"
MINMAX_SCALER = "minmax"

SUPPORTED_SCALERS = {
    STANDARD_SCALER,
    MINMAX_SCALER,
}

# ==========================================================
# Rolling Window Sizes
# ==========================================================

WINDOW_1H = "1h"
WINDOW_6H = "6h"
WINDOW_24H = "24h"

DEFAULT_ROLLING_WINDOW = WINDOW_1H

# ==========================================================
# Alert Severity
# ==========================================================

ALERT_SEVERITIES = [
    "Low",
    "Medium",
    "High",
    "Critical",
]

# ==========================================================
# Health Status
# ==========================================================

HEALTHY = "Healthy"
WARNING = "Warning"
CRITICAL = "Critical"
OFFLINE = "Offline"

# ==========================================================
# Agent Status
# ==========================================================

ONLINE = "Online"
OFFLINE_AGENT = "Offline"

# ==========================================================
# Export Formats
# ==========================================================

CSV = "csv"
PARQUET = "parquet"

SUPPORTED_EXPORTS = [
    CSV,
    PARQUET,
]