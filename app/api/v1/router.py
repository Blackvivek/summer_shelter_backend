from fastapi import APIRouter

from app.api.v1 import animals, adoptions, statistics

api_router = APIRouter()
api_router.include_router(animals.router, prefix="/animals", tags=["animals"])
api_router.include_router(adoptions.router, prefix="/adoptions", tags=["adoptions"])
# api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])

# Additional routers will be included here as the application grows