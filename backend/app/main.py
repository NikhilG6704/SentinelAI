from fastapi import FastAPI

app = FastAPI(
    title="SentinelAI API",
    description="Backend API for SentinelAI - Autonomous Self-Healing Enterprise Infrastructure Platform",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "application": "SentinelAI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }