from fastapi import FastAPI
from app.api.routers import router as api_router
from app.core.db import init_db

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
async def health_check():
    return {"status": "ok"}
