"""Runs both services for manual testing: python -m app.main

Service A: http://127.0.0.1:8001/docs
Service B: http://127.0.0.1:8002/docs
"""
import subprocess
import sys

# uvicorn target and port for each service
SERVICES = {
    "app.services.service_a:app": 8001,
    "app.services.service_b:app": 8002,
}


def start(target, port):
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", target, "--port", str(port), "--log-level", "warning"]
    )


if __name__ == "__main__":
    processes = [start(target, port) for target, port in SERVICES.items()]
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
