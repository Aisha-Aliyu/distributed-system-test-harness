from fastapi import FastAPI
import time
import random

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/process")
def process():
    time.sleep(random.uniform(0.1, 1.5))  # simulate latency
    return {"service": "A", "result": "success"}