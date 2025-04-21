from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import computed_field


class AnimalBase(SQLModel):
    """Base schema for animal data"""
    name: str
    type: str
    age: float
    breed: str
    gender: Optional[str] = None
    health_status: str
    description: str


class Animal(AnimalBase, table=True):
    """Animal model for database storage"""
    id: Optional[int] = Field(default=None, primary_key=True)
    image_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_adopted: bool = False


class AnimalCreate(AnimalBase):
    """Schema for creating a new animal"""
    image_path: Optional[str] = None


class AnimalRead(AnimalBase):
    """Schema for reading animal data"""
    id: int
    image_path: Optional[str] = None
    created_at: datetime
    is_adopted: bool
    
    @computed_field
    def image_url(self) -> Optional[str]:
        """Get the full URL for the image"""
        if not self.image_path:
            return None
        # Return the complete URL path that can be used by the frontend
        # This assumes your API is running on localhost:8000
        return f"http://localhost:8000/{self.image_path}"


class AnimalUpdate(SQLModel):
    """Schema for updating animal data with optional fields"""
    name: Optional[str] = None
    type: Optional[str] = None
    age: Optional[float] = None
    breed: Optional[str] = None
    gender: Optional[str] = None
    health_status: Optional[str] = None
    description: Optional[str] = None
    image_path: Optional[str] = None
    is_adopted: Optional[bool] = None
