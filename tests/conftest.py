# Starts both services before the tests and stops them afterwards, so `pytest` is all
# it takes to run the suite
import time

import pytest
import requests

from app.main import SERVICES, start


def wait_until_up(port, timeout=20):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if requests.get(f"http://127.0.0.1:{port}/health", timeout=1).status_code == 200:
                return
        except requests.ConnectionError:
            pass
        time.sleep(0.2)
    raise RuntimeError(f"The service on port {port} didn't start")


@pytest.fixture(scope="session", autouse=True)
def services():
    processes = [start(target, port) for target, port in SERVICES.items()]
    try:
        for port in SERVICES.values():
            wait_until_up(port)
        yield
    finally:
        for process in processes:
            process.terminate()
            process.wait(timeout=10)
