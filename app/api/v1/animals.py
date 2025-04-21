from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
import shutil
import os
from pathlib import Path
from sqlmodel import Session

from app.db.database import get_session
from app.schemas.animal import AnimalCreate, AnimalRead, AnimalUpdate, Animal
from app.services.animal_service import AnimalService

router = APIRouter()

# Configuration for file uploads
UPLOAD_DIRECTORY = Path("uploads/animals")
# Create the directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.post("/", response_model=AnimalRead)
async def create_animal(
    name: str = Form(...),
    type: str = Form(...),
    age: float = Form(...),
    breed: str = Form(...),
    gender: Optional[str] = Form(None),
    health_status: str = Form(...),
    description: str = Form(...),
    image: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session)
):
    """Create a new animal record with optional image upload"""
    # Initialize the service
    service = AnimalService(session)
    
    # Handle image upload if provided
    image_path = None
    if image:
        # Create a unique filename
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{name}_{os.urandom(8).hex()}{file_extension}"
        file_path = UPLOAD_DIRECTORY / unique_filename
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        # Store the relative path instead of full path
        image_path = f"uploads/animals/{unique_filename}"

    # Create the animal record
    animal_data = {
        "name": name,
        "type": type,
        "age": age,
        "breed": breed,
        "gender": gender,
        "health_status": health_status,
        "description": description,
        "image_path": image_path
    }
    
    new_animal = AnimalCreate(**animal_data)
    return service.create_animal(new_animal)


@router.get("/{animal_id}", response_model=AnimalRead)
def get_animal(
    animal_id: int, 
    session: Session = Depends(get_session)
):
    """Get a specific animal by ID"""
    service = AnimalService(session)
    return service.get_animal(animal_id)


@router.get("/", response_model=List[AnimalRead])
def get_animals(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    name: Optional[str] = Query(None, description="Filter by animal name"),
    type: Optional[str] = Query(None, description="Filter by animal type"),
    breed: Optional[str] = Query(None, description="Filter by animal breed"),
    is_adopted: Optional[bool] = Query(None, description="Filter by adoption status")
):
    """Get a list of animals with optional filtering"""
    service = AnimalService(session)
    
    # If any search parameters are provided, use search method
    if any([name, type, breed, is_adopted is not None]):
        return service.search_animals(name, type, breed, is_adopted)
    
    # Otherwise, get all animals with pagination
    return service.get_animals(skip, limit)


@router.put("/{animal_id}", response_model=AnimalRead)
async def update_animal(
    animal_id: int,
    name: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    age: Optional[float] = Form(None),
    breed: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    health_status: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    is_adopted: Optional[bool] = Form(None),
    session: Session = Depends(get_session)
):
    """Update an existing animal record"""
    # Initialize the service
    service = AnimalService(session)
    
    # Handle image upload if provided
    image_path = None
    if image:
        # Create a unique filename
        file_extension = os.path.splitext(image.filename)[1]
        name_part = name or f"animal_{animal_id}" 
        unique_filename = f"{name_part}_{os.urandom(8).hex()}{file_extension}"
        file_path = UPLOAD_DIRECTORY / unique_filename
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        # Store the relative path instead of full path
        image_path = f"uploads/animals/{unique_filename}"

    # Update the animal record
    update_data = {
        "name": name,
        "type": type,
        "age": age,
        "breed": breed,
        "gender": gender,
        "health_status": health_status,
        "description": description,
        "is_adopted": is_adopted
    }
    
    # Only include image_path if a new image was uploaded
    if image_path:
        update_data["image_path"] = image_path
    
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    animal_update = AnimalUpdate(**update_data)
    return service.update_animal(animal_id, animal_update)


@router.delete("/{animal_id}", response_model=dict)
def delete_animal(
    animal_id: int, 
    session: Session = Depends(get_session)
):
    """Delete an animal record"""
    service = AnimalService(session)
    service.delete_animal(animal_id)
    return {"message": f"Animal with ID {animal_id} deleted successfully"}


@router.patch("/{animal_id}/adopt", response_model=AnimalRead)
def mark_as_adopted(
    animal_id: int, 
    session: Session = Depends(get_session)
):
    """Mark an animal as adopted"""
    service = AnimalService(session)
    return service.mark_as_adopted(animal_id)