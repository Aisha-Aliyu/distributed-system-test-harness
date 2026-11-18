# Distributed System Test Harness

Two small FastAPI services and a pytest suite that checks how they behave together: health checks, response times under concurrent load, and a service that sometimes reports itself as degraded.

- Service A (port 8001): `/health`, and `/process`, which takes 0.1 to 1.5 seconds to answer, like a slow downstream call.
- Service B (port 8002): `/health`, which reports `degraded` about one time in five.

## Run the tests

```bash
pip install -r requirements.txt
pytest -v
```

The tests start both services themselves and stop them when they finish. They also run on every push and pull request with GitHub Actions.

## Run the services yourself

```bash
python -m app.main
```

Then open http://127.0.0.1:8001/docs or http://127.0.0.1:8002/docs. Press Ctrl+C to stop both.
