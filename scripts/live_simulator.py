#!/usr/bin/env python3
"""
SentinelAI — 5-Server Multi-Instance Panel Demo
Simulates 5 monitored infrastructure nodes. All run healthy in parallel.
The presenter picks one server to crash — the AI detects it, diagnoses it,
and self-heals it while the other 4 stay green the entire time.
"""
import time
import random
import requests
import threading

API_BASE = "http://localhost:8000"
API_URL  = f"{API_BASE}/api/v1"

# 5 simulated server definitions
SERVERS = [
    {"name": "web-srv-01", "ip": "10.0.0.11"},
    {"name": "web-srv-02", "ip": "10.0.0.12"},
    {"name": "db-cluster", "ip": "10.0.0.20"},
    {"name": "cache-srv",  "ip": "10.0.0.30"},
    {"name": "api-gw-01",  "ip": "10.0.0.40"},
]

# Per-server state: "NORMAL", "CRASH", "RESTORED"
server_states = {s["name"]: "NORMAL" for s in SERVERS}
# Stores created agent IDs for each server name
agents = {}
assets = {}
automation_rule_id = None


# ---------------------------------------------------------------------------
# Bootstrap helpers
# ---------------------------------------------------------------------------

def bootstrap_servers():
    """Create (or reuse) all 5 infrastructure assets + monitoring agents."""
    print("\nBootstrapping 5 server instances...")

    existing_assets = requests.get(f"{API_URL}/infrastructure-assets?skip=0&limit=50").json().get("data", [])
    asset_by_hostname = {a["hostname"]: a for a in existing_assets}

    existing_agents = requests.get(f"{API_URL}/monitoring-agents?skip=0&limit=50").json().get("data", [])
    agent_by_asset = {ag["infrastructure_asset_id"]: ag for ag in existing_agents}

    for srv in SERVERS:
        name = srv["name"]

        # Asset
        if name in asset_by_hostname:
            asset_id = asset_by_hostname[name]["id"]
        else:
            res = requests.post(f"{API_URL}/infrastructure-assets", json={
                "hostname": name,
                "ip_address": srv["ip"],
                "operating_system": "Ubuntu 22.04 LTS",
                "asset_type": "Server",
                "environment": "Production",
                "status": "Healthy",
                "location": "us-east-1a",
                "description": f"Simulated {name} for SentinelAI demo",
            })
            data = res.json()
            if "data" not in data:
                print(f"  ❌ Failed to create asset {name}: {data}")
                continue
            asset_id = data["data"]["id"]

        assets[name] = asset_id

        # Agent
        if asset_id in agent_by_asset:
            agent_id = agent_by_asset[asset_id]["id"]
        else:
            res = requests.post(f"{API_URL}/monitoring-agents/register", json={
                "infrastructure_asset_id": asset_id,
                "agent_name": f"agent-{name}",
                "agent_version": "2.1.0",
            })
            data = res.json()
            if "data" not in data:
                print(f"  ❌ Failed to create agent for {name}: {data}")
                continue
            agent_id = data["data"]["id"]

        agents[name] = agent_id
        print(f"  ✅ {name:15s} → asset_id={asset_id}, agent_id={agent_id}")

    print("All 5 servers registered.\n")


def get_or_create_automation_rule():
    global automation_rule_id
    res = requests.get(f"{API_URL}/automation-rules?skip=0&limit=1")
    data = res.json().get("data", [])
    if data:
        automation_rule_id = data[0]["id"]
        return
    res = requests.post(f"{API_URL}/automation-rules", json={
        "rule_name": "Emergency Service Restart",
        "condition_expression": "cpu > 90",
        "action_type": "RestartService",
        "action_payload": {"service": "auto"},
        "is_enabled": True,
    })
    automation_rule_id = res.json()["data"]["id"]


# ---------------------------------------------------------------------------
# Background metrics threads
# ---------------------------------------------------------------------------

def metrics_thread(server_name: str, agent_id: int):
    """Continuously push metrics for a single server based on its state."""
    while True:
        state = server_states[server_name]

        if state in ("NORMAL", "RESTORED"):
            cpu = random.uniform(12.0, 28.0)
            mem = random.uniform(35.0, 55.0)
        elif state == "CRASH":
            cpu = random.uniform(95.0, 100.0)
            mem = random.uniform(92.0, 99.0)
        else:
            cpu, mem = 20.0, 40.0

        try:
            requests.post(f"{API_URL}/system-metrics", json={
                "monitoring_agent_id": agent_id,
                "cpu_usage": round(cpu, 1),
                "memory_usage": round(mem, 1),
                "disk_usage": round(random.uniform(40.0, 60.0), 1),
                "network_in": round(random.uniform(50, 400), 1),
                "network_out": round(random.uniform(50, 400), 1),
                "uptime_seconds": 3600,
            }, timeout=3)
        except Exception:
            pass  # Ignore transient errors

        time.sleep(2)


def start_all_metric_threads():
    for name, agent_id in agents.items():
        t = threading.Thread(target=metrics_thread, args=(name, agent_id), daemon=True)
        t.start()
    print("📡 Metrics streaming for all 5 servers (every 2 seconds).\n")


# ---------------------------------------------------------------------------
# AI & Incident pipeline for the crashed server
# ---------------------------------------------------------------------------

def run_ai_pipeline(crashed_server: str):
    asset_id  = assets[crashed_server]
    agent_id  = agents[crashed_server]

    print(f"\n🔍 Running AI Anomaly Detection on {crashed_server}...")
    requests.post(f"{API_URL}/ai/detect-anomaly", json={"monitoring_agent_id": agent_id})

    print(f"🚨 Creating Critical Incident for {crashed_server}...")
    res = requests.post(f"{API_URL}/incidents", json={
        "infrastructure_asset_id": asset_id,
        "monitoring_agent_id": agent_id,
        "incident_title": f"CPU Saturation Detected on {crashed_server}",
        "incident_description": (
            f"SentinelAI detected anomalous CPU and memory patterns on {crashed_server}. "
            "Behavior matches historical resource exhaustion events."
        ),
        "severity": "Critical",
    })
    incident_id = res.json()["data"]["id"]
    print(f"   → Incident #{incident_id} created.")

    print("🧠 Querying AI Root Cause Analysis...")
    rca_res = requests.post(f"{API_URL}/ai/root-cause", json={"incident_id": incident_id})
    probable_cause = rca_res.json()["data"]["probable_cause"]

    print("💡 Querying AI Recommendation...")
    rec_res = requests.post(f"{API_URL}/ai/recommendation", json={"incident_id": incident_id})
    recommendation = rec_res.json()["data"]["recommended_action"]

    # Update the incident with AI findings
    requests.put(f"{API_URL}/incidents/{incident_id}", json={
        "incident_description": (
            f"SentinelAI detected anomalous CPU and memory patterns on {crashed_server}.\n\n"
            f"Root Cause: {probable_cause}\n"
            f"Recommendation: {recommendation}"
        )
    })

    print(f"\n{'='*50}")
    print(f"🔍 ROOT CAUSE   : {probable_cause}")
    print(f"💡 RECOMMENDATION: {recommendation}")
    print(f"{'='*50}")

    return incident_id, probable_cause, recommendation


def run_healing_pipeline(crashed_server: str, incident_id: int):
    asset_id = assets[crashed_server]

    print(f"\n🛠️  Creating Self-Healing Workflow for {crashed_server}...")
    res = requests.post(f"{API_URL}/recovery-workflows", json={
        "workflow_name": f"Auto-Heal {crashed_server} — Incident #{incident_id}",
        "automation_rule_id": automation_rule_id,
        "incident_id": incident_id,
        "infrastructure_asset_id": asset_id,
        "action_type": "RESTART_SERVICE",
        "executed_by": "SentinelAI Automation Engine",
    })

    data = res.json()
    if "data" not in data:
        print(f"Error creating workflow: {data}")
        return None

    workflow_id = data["data"]["id"]
    print(f"   → Workflow #{workflow_id} created (Pending).")

    input("\n👉  Press ENTER to EXECUTE the recovery workflow...")

    print("⚙️  Executing Recovery Workflow...")
    requests.post(f"{API_URL}/recovery-workflows/{workflow_id}/execute")
    print(f"   → Workflow #{workflow_id} is now Executing...")

    time.sleep(3)  # simulate execution time

    print(f"\n✅ Restoring {crashed_server} to healthy state...")
    server_states[crashed_server] = "RESTORED"

    print("📝 Resolving Incident...")
    requests.post(f"{API_URL}/incidents/{incident_id}/resolve", json={
        "resolution_summary": (
            f"SentinelAI automatically executed a service restart on {crashed_server}. "
            "CPU normalized to ~20%. System health confirmed."
        )
    })

    print(f"\n{'='*50}")
    print(f"✅ {crashed_server} HEALED — incident resolved!")
    print(f"{'='*50}")

    return workflow_id


# ---------------------------------------------------------------------------
# Main presenter flow
# ---------------------------------------------------------------------------

def print_server_status():
    print("\n📊 Current Server Status:")
    print(f"{'Server':<15}  {'State':<10}  {'Agent ID'}")
    print("-" * 40)
    for name in [s["name"] for s in SERVERS]:
        state = server_states[name]
        icon = "✅" if state == "NORMAL" else ("🔥" if state == "CRASH" else "💚")
        agent_id = agents.get(name, "N/A")
        print(f"  {icon} {name:<13}  {state:<10}  {agent_id}")
    print()


def main():
    print("Checking backend connectivity...")
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        r.raise_for_status()
    except Exception:
        print("❌ Error: Backend is not running on localhost:8000")
        print("Start it with: cd backend && venv/bin/python -m uvicorn app.main:app --reload")
        return

    bootstrap_servers()
    get_or_create_automation_rule()
    start_all_metric_threads()

    print("=" * 55)
    print("🎬  SENTINELAI — 5-SERVER PANEL REVIEW DEMO 🎬")
    print("=" * 55)
    print_server_status()

    print("All 5 servers are now streaming healthy metrics to the dashboard.")
    print("Open the SentinelAI dashboard in your browser and show the panel.")
    print()

    # Let the presenter choose the server to crash
    print("Available servers to crash:")
    for i, srv in enumerate(SERVERS, 1):
        print(f"  {i}. {srv['name']}")

    choice = input("\n👉  Enter server number to crash [default: 3 (db-cluster)]: ").strip()
    try:
        idx = int(choice) - 1 if choice else 2
        crashed_server = SERVERS[idx]["name"]
    except (ValueError, IndexError):
        crashed_server = "db-cluster"

    input(f"\n👉  Press ENTER to crash '{crashed_server}'...")

    # Phase: CRASH
    print(f"\n💥 Injecting failure into {crashed_server}...")
    server_states[crashed_server] = "CRASH"
    print(f"   → {crashed_server} CPU is now spiking to ~99%")
    print("   → Other 4 servers remain healthy.\n")

    input("👉  Press ENTER once the crash shows in the dashboard, then AI will diagnose...")

    # Phase: AI PIPELINE
    incident_id, probable_cause, recommendation = run_ai_pipeline(crashed_server)

    input("\n👉  Press ENTER to point out the AI findings on the dashboard, then start Self-Healing...")

    # Phase: HEALING
    run_healing_pipeline(crashed_server, incident_id)

    print_server_status()
    print("🎉 Demo complete! You can press Ctrl+C to stop the simulator.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    main()
