from fastapi import APIRouter
from app.api.v1.endpoints import auth, detection, history, knowledge

api_router = APIRouter()

@api_router.get("/health-check")
async def health_check_v1():
    return {
        "status": "healthy",
        "message": "Grovia API + ML Detection Ready! 🧠🚀"
    }

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    detection.router,
    prefix="/detection",
    tags=["Plant Disease Detection"]
)

api_router.include_router(
    history.router,
    prefix="/history",
    tags=["History"]
)

api_router.include_router(
    knowledge.router,
    prefix="/knowledge",
    tags=["Knowledge Base"]
)