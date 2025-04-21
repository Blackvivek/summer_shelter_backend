from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException

from app.schemas.animal import Animal, AnimalCreate, AnimalUpdate


class AnimalService:
    def __init__(self, session: Session):
        self.session = session

    def create_animal(self, animal: AnimalCreate) -> Animal:
        """Create a new animal record"""
        # Create a dictionary with all fields from the AnimalCreate instance
        animal_data = animal.model_dump()
        
        # Create a new Animal instance with all fields, including image_path
        db_animal = Animal(**animal_data)
        
        self.session.add(db_animal)
        self.session.commit()
        self.session.refresh(db_animal)
        return db_animal

    def get_animal(self, animal_id: int) -> Animal:
        """Get a single animal by ID"""
        animal = self.session.get(Animal, animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail=f"Animal with ID {animal_id} not found")
        return animal

    def get_animals(self, skip: int = 0, limit: int = 100) -> List[Animal]:
        """Get multiple animals with pagination"""
        animals = self.session.exec(
            select(Animal).offset(skip).limit(limit)
        ).all()
        return animals

    def update_animal(self, animal_id: int, animal_update: AnimalUpdate) -> Animal:
        """Update an existing animal"""
        db_animal = self.get_animal(animal_id)
        
        update_data = animal_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_animal, key, value)
            
        # Always update the updated_at timestamp when changes are made
        from datetime import datetime
        db_animal.updated_at = datetime.utcnow()
        
        self.session.add(db_animal)
        self.session.commit()
        self.session.refresh(db_animal)
        return db_animal

    def delete_animal(self, animal_id: int) -> None:
        """Delete an animal"""
        animal = self.get_animal(animal_id)
        self.session.delete(animal)
        self.session.commit()
        
    def search_animals(self, name: Optional[str] = None, animal_type: Optional[str] = None, 
                       breed: Optional[str] = None, is_adopted: Optional[bool] = None) -> List[Animal]:
        """Search animals by various criteria"""
        query = select(Animal)
        
        if name:
            query = query.where(Animal.name.contains(name))
        if animal_type:
            query = query.where(Animal.type == animal_type)
        if breed:
            query = query.where(Animal.breed.contains(breed))
        if is_adopted is not None:  # Checking None specifically because it's a boolean
            query = query.where(Animal.is_adopted == is_adopted)
            
        return self.session.exec(query).all()
        
    def mark_as_adopted(self, animal_id: int) -> Animal:
        """Mark an animal as adopted"""
        animal = self.get_animal(animal_id)
        animal.is_adopted = True
        from datetime import datetime
        animal.updated_at = datetime.utcnow()
        self.session.add(animal)
        self.session.commit()
        self.session.refresh(animal)
        return animal