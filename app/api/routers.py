from fastapi import APIRouter
from app.api.v1.routers import router as v1_router


router = APIRouter(prefix="/api", tags=["api"])

router.include_router(v1_router)
