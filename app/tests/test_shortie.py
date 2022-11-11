from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_shorten_url():
    long_url = "https://example.com"
    response = client.post("shortie", json={"long_url": long_url})
    assert response.status_code == 200
    assert long_url in response.json().values()
