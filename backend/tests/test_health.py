def test_root(client):
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["status"] == "running"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["status"] == "healthy"