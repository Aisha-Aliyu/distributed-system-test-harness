import time
from concurrent.futures import ThreadPoolExecutor

import requests

SERVICE_A = "http://127.0.0.1:8001"
SERVICE_B = "http://127.0.0.1:8002"
TIMEOUT = 5  # seconds; a call that hangs fails the test instead of blocking the run


def test_service_health():
    response_a = requests.get(f"{SERVICE_A}/health", timeout=TIMEOUT)
    response_b = requests.get(f"{SERVICE_B}/health", timeout=TIMEOUT)

    assert response_a.status_code == 200
    assert response_b.status_code == 200


def timed_process(_):
    start = time.time()
    response = requests.get(f"{SERVICE_A}/process", timeout=TIMEOUT)
    return response, time.time() - start


def test_latency_under_load():
    # 10 requests at once; each one should still answer within 2 seconds
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(timed_process, range(10)))

    for response, duration in results:
        assert response.status_code == 200
        assert response.json() == {"service": "A", "result": "success"}
        assert duration < 2.0


def test_degraded_service_still_answers():
    # Service B reports "degraded" about one time in five, but it should always answer
    statuses = [
        requests.get(f"{SERVICE_B}/health", timeout=TIMEOUT).json()["status"]
        for _ in range(30)
    ]
    assert set(statuses) <= {"ok", "degraded"}
