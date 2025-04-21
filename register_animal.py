import requests
import os

def register_animal():
    """
    Script to register a new animal to the database using the FastAPI endpoint.
    
    This script sends form data (multipart/form-data) to the API which is required
    by the endpoint that accepts file uploads.
    """
    # API URL
    url = "http://localhost:8000/api/v1/animals/"
    
    # Animal data - all required fields must be provided
    form_data = {
        "name": "Buddy",
        "type": "Dog",
        "age": 2.5,
        "breed": "Labrador Retriever",
        "gender": "Male",  # Optional field
        "health_status": "Healthy",
        "description": "Friendly and energetic dog who loves to play fetch."
    }
    
    # Optional: Path to an image file to upload
    image_path = None  # Change this to a real path if you want to upload an image
    
    # Prepare the files dict for requests if an image is provided
    files = {}
    if image_path and os.path.exists(image_path):
        files = {
            "image": (os.path.basename(image_path), open(image_path, "rb"), "image/jpeg")
        }
    
    try:
        # Send the request with form data and optional file
        response = requests.post(url, data=form_data, files=files)
        
        # Check if request was successful
        if response.status_code == 200:
            animal_data = response.json()
            print("✅ Animal registered successfully!")
            print(f"Animal ID: {animal_data.get('id')}")
            print(f"Name: {animal_data.get('name')}")
            print(f"Type: {animal_data.get('type')}")
            print(f"Breed: {animal_data.get('breed')}")
        else:
            print(f"❌ Error: Status code {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        
    if "image" in files:
        files["image"][1].close()  # Close the file if it was opened


if __name__ == "__main__":
    register_animal()