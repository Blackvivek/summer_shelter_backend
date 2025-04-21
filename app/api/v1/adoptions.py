from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.adoption import AdoptionCreate, AdoptionRead, AdoptionUpdate, Adoption, HousingSituation, HomeOwnership
from app.services.adoption_service import AdoptionService
from app.schemas.animal import Animal

router = APIRouter()


@router.post("/", response_model=AdoptionRead)
async def create_adoption_application(
    adoption: AdoptionCreate,
    session: Session = Depends(get_session)
):
    """Submit a new adoption application"""
    service = AdoptionService(session)
    return service.create_adoption(adoption)


@router.get("/{adoption_id}", response_model=AdoptionRead)
def get_adoption_application(
    adoption_id: int, 
    session: Session = Depends(get_session)
):
    """Get a specific adoption application by ID"""
    service = AdoptionService(session)
    return service.get_adoption(adoption_id)


@router.get("/", response_model=List[AdoptionRead])
def get_adoption_applications(
    skip: int = 0, 
    limit: int = 100, 
    animal_id: Optional[int] = Query(None, description="Filter by animal ID"),
    status: Optional[str] = Query(None, description="Filter by application status"),
    session: Session = Depends(get_session)
):
    """Get a list of adoption applications with optional filtering"""
    service = AdoptionService(session)
    
    if animal_id is not None:
        return service.get_adoptions_by_animal(animal_id)
    elif status is not None:
        return service.get_adoptions_by_status(status)
    else:
        return service.get_adoptions(skip, limit)


@router.put("/{adoption_id}", response_model=AdoptionRead)
def update_adoption_application(
    adoption_id: int,
    adoption: AdoptionUpdate,
    session: Session = Depends(get_session)
):
    """Update an existing adoption application"""
    service = AdoptionService(session)
    return service.update_adoption(adoption_id, adoption)


@router.delete("/{adoption_id}", response_model=dict)
def delete_adoption_application(
    adoption_id: int, 
    session: Session = Depends(get_session)
):
    """Delete an adoption application"""
    service = AdoptionService(session)
    service.delete_adoption(adoption_id)
    return {"message": f"Adoption application with ID {adoption_id} deleted successfully"}


@router.patch("/{adoption_id}/approve", response_model=AdoptionRead)
def approve_adoption_application(
    adoption_id: int, 
    session: Session = Depends(get_session)
):
    """Approve an adoption application and mark the animal as adopted"""
    service = AdoptionService(session)
    return service.approve_adoption(adoption_id)


@router.patch("/{adoption_id}/reject", response_model=AdoptionRead)
def reject_adoption_application(
    adoption_id: int, 
    session: Session = Depends(get_session)
):
    """Reject an adoption application"""
    service = AdoptionService(session)
    return service.reject_adoption(adoption_id)


@router.get("/housing-options", response_model=dict)
def get_housing_options():
    """Get available housing situation options for the form"""
    return {
        "housing_situations": [situation.value for situation in HousingSituation],
        "home_ownership": [ownership.value for ownership in HomeOwnership]
    }