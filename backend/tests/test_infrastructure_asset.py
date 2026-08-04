import uuid


def test_create_asset(client):
    unique = str(uuid.uuid4())[:8]

    payload = {
        "hostname": f"server-{unique}",
        "ip_address": "192.168.10.10",
        "operating_system": "Ubuntu 24.04",
        "asset_type": "Server",
        "environment": "Production",
        "status": "Healthy",
        "location": "Mumbai",
        "description": "Test Server"
    }

    response = client.post(
        "/api/v1/infrastructure-assets",
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True
    assert body["data"]["hostname"] == payload["hostname"]


def test_get_assets(client):
    response = client.get("/api/v1/infrastructure-assets")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_get_invalid_asset(client):
    response = client.get("/api/v1/infrastructure-assets/999999")

    assert response.status_code == 404


def test_invalid_ip_validation(client):
    payload = {
        "hostname": "invalid-ip",
        "ip_address": "999.999.999.999",
        "operating_system": "Ubuntu",
        "asset_type": "Server",
        "environment": "Production",
        "status": "Healthy",
        "location": "Mumbai",
        "description": ""
    }

    response = client.post(
        "/api/v1/infrastructure-assets",
        json=payload,
    )

    assert response.status_code == 422