from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException

from app.schemas.adoption import Adoption, AdoptionCreate, AdoptionUpdate
from app.schemas.animal import Animal


class AdoptionService:
    def __init__(self, session: Session):
        self.session = session

    def create_adoption(self, adoption: AdoptionCreate) -> Adoption:
        """Create a new adoption application"""
        # Verify that the animal exists
        animal = self.session.get(Animal, adoption.animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail=f"Animal with ID {adoption.animal_id} not found")
        
        # Check if animal is already adopted
        if animal.is_adopted:
            raise HTTPException(status_code=400, detail=f"Animal with ID {adoption.animal_id} is already adopted")

        # Create the adoption application
        db_adoption = Adoption.model_validate(adoption.model_dump())
        self.session.add(db_adoption)
        
        # Mark animal as adopted immediately
        animal.is_adopted = True
        self.session.add(animal)
        
        self.session.commit()
        self.session.refresh(db_adoption)
        return db_adoption

    def get_adoption(self, adoption_id: int) -> Adoption:
        """Get a single adoption application by ID"""
        adoption = self.session.get(Adoption, adoption_id)
        if not adoption:
            raise HTTPException(status_code=404, detail=f"Adoption application with ID {adoption_id} not found")
        return adoption

    def get_adoptions(self, skip: int = 0, limit: int = 100) -> List[Adoption]:
        """Get multiple adoption applications with pagination"""
        adoptions = self.session.exec(
            select(Adoption).offset(skip).limit(limit)
        ).all()
        return adoptions

    def get_adoptions_by_animal(self, animal_id: int) -> List[Adoption]:
        """Get all adoption applications for a specific animal"""
        adoptions = self.session.exec(
            select(Adoption).where(Adoption.animal_id == animal_id)
        ).all()
        return adoptions

    def get_adoptions_by_status(self, status: str) -> List[Adoption]:
        """Get all adoption applications with a specific status"""
        adoptions = self.session.exec(
            select(Adoption).where(Adoption.status == status)
        ).all()
        return adoptions

    def update_adoption(self, adoption_id: int, adoption_update: AdoptionUpdate) -> Adoption:
        """Update an existing adoption application"""
        db_adoption = self.get_adoption(adoption_id)
        
        update_data = adoption_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_adoption, key, value)
            
        self.session.add(db_adoption)
        self.session.commit()
        self.session.refresh(db_adoption)
        return db_adoption

    def delete_adoption(self, adoption_id: int) -> None:
        """Delete an adoption application"""
        adoption = self.get_adoption(adoption_id)
        self.session.delete(adoption)
        self.session.commit()
        
    def approve_adoption(self, adoption_id: int) -> Adoption:
        """Approve an adoption application and mark the animal as adopted"""
        adoption = self.get_adoption(adoption_id)
        
        # Get the animal
        animal = self.session.get(Animal, adoption.animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail=f"Animal with ID {adoption.animal_id} not found")
            
        # Check if animal is already adopted
        if animal.is_adopted:
            raise HTTPException(status_code=400, detail=f"Animal with ID {adoption.animal_id} is already adopted")
            
        # Update adoption status
        adoption.status = "Approved"
        
        # Mark animal as adopted
        animal.is_adopted = True
        
        # Save changes
        self.session.add(adoption)
        self.session.add(animal)
        self.session.commit()
        self.session.refresh(adoption)
        
        return adoption
        
    def reject_adoption(self, adoption_id: int) -> Adoption:
        """Reject an adoption application"""
        adoption = self.get_adoption(adoption_id)
        adoption.status = "Rejected"
        self.session.add(adoption)
        self.session.commit()
        self.session.refresh(adoption)
        return adoption