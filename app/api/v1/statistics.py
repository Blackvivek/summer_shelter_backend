from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.database import get_session
from app.services.statistics_service import StatisticsService

router = APIRouter()

@router.get("/")
async def get_shelter_statistics(session: Session = Depends(get_session)):
    """Get shelter statistics summary"""
    service = StatisticsService(session)
    return service.get_summary_statistics()

@router.get("/adoptions")
async def get_adoption_statistics(session: Session = Depends(get_session)):
    """Get detailed adoption statistics"""
    service = StatisticsService(session)
    return service.get_adoption_statistics()

@router.get("/animal-types")
async def get_animal_type_distribution(session: Session = Depends(get_session)):
    """Get distribution of animals by type"""
    service = StatisticsService(session)
    return service.get_animal_type_distribution()

@router.get("/fallback")
async def get_fallback_statistics():
    """Get hardcoded shelter statistics (for demonstration or fallback)"""
    return {
        "total_animals": 300,
        "new_admissions": 50,
        "adopted_animals": 120,
        "rescued_animals": 150
    }
