from app.schemas import HealthResponse
from app.version import VERSION
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(ok=True, version=VERSION)
