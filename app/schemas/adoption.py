from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum


class HousingSituation(str, Enum):
    """Enum for housing situation options"""
    HOUSE = "House"
    APARTMENT = "Apartment" 
    CONDO = "Condo"
    MOBILE_HOME = "Mobile Home"
    OTHER = "Other"


class HomeOwnership(str, Enum):
    """Enum for home ownership options"""
    OWN = "Own"
    RENT = "Rent"
    OTHER = "Other"


class AdoptionBase(SQLModel):
    """Base schema for adoption application data"""
    full_name: str
    email: str
    phone: str
    address: str
    housing_situation: HousingSituation
    home_ownership: HomeOwnership  # Own or rent
    has_other_pets: Optional[bool] = None
    previous_pet_experience: Optional[str] = None
    adoption_reason: str
    animal_id: int = Field(foreign_key="animal.id")


class Adoption(AdoptionBase, table=True):
    """Adoption model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "Pending"  # Pending, Approved, Rejected


class AdoptionCreate(AdoptionBase):
    """Schema for creating a new adoption application"""
    pass


class AdoptionRead(AdoptionBase):
    """Schema for reading adoption application data"""
    id: int
    created_at: datetime
    status: str


class AdoptionUpdate(SQLModel):
    """Schema for updating adoption application data with optional fields"""
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    housing_situation: Optional[HousingSituation] = None
    home_ownership: Optional[HomeOwnership] = None
    has_other_pets: Optional[bool] = None
    previous_pet_experience: Optional[str] = None
    adoption_reason: Optional[str] = None
    animal_id: Optional[int] = None
    status: Optional[str] = None