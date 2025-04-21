from app.db.database import get_session, engine
from app.schemas.animal import AnimalCreate
from app.services.animal_service import AnimalService
from sqlmodel import Session

def test_image_path():
    """Test if image_path is being stored and retrieved correctly"""
    
    # Use a direct session for testing
    with Session(engine) as session:
        # Create a service
        service = AnimalService(session)
        
        # Create test animal data with an image path
        animal_data = AnimalCreate(
            name="TestDog",
            type="Dog",
            age=2.5,
            breed="Test Breed",
            gender="Male",
            health_status="Healthy",
            description="A test animal to verify image path storage"
        )
        
        # Create the animal and manually set image path
        animal = service.create_animal(animal_data)
        animal.image_path = "uploads/animals/test_image.jpg"
        session.add(animal)
        session.commit()
        session.refresh(animal)
        
        # Print the animal record to verify image_path is stored
        print("\n=== CREATED ANIMAL ===")
        print(f"ID: {animal.id}")
        print(f"Name: {animal.name}")
        print(f"Image Path: {animal.image_path}")
        
        # Retrieve the animal from the database
        retrieved_animal = service.get_animal(animal.id)
        
        # Print the retrieved animal to verify image_path is returned
        print("\n=== RETRIEVED ANIMAL ===")
        print(f"ID: {retrieved_animal.id}")
        print(f"Name: {retrieved_animal.name}")
        print(f"Image Path: {retrieved_animal.image_path}")
        
        # Clean up the test data
        session.delete(animal)
        session.commit()
        
        return animal.image_path == retrieved_animal.image_path

if __name__ == "__main__":
    result = test_image_path()
    print(f"\nTest passed: {result}")