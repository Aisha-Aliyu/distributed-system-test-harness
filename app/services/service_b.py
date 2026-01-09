from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/health")
def health():
    if random.random() < 0.2:
        return {"status": "degraded"}
    return {"status": "ok"}