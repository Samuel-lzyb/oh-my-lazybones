"""oh-my-lazybones API Server"""
from fastapi import FastAPI

app = FastAPI(title="oh-my-lazybones", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}