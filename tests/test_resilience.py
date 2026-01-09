import requests
import time

SERVICE_A = "http://localhost:8001"
SERVICE_B = "http://localhost:8002"

def test_service_health():
    response_a = requests.get(f"{SERVICE_A}/health")
    response_b = requests.get(f"{SERVICE_B}/health")

    assert response_a.status_code == 200
    assert response_b.status_code == 200

def test_latency_under_load():
    start = time.time()
    response = requests.get(f"{SERVICE_A}/process")
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 2.0 
    