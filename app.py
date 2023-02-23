import face_recognition
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# In-memory database to store registered faces
database = {}

# Register endpoint
@app.post('/register/')
async def register(name: str, email: str, file: UploadFile=File()):
    # Read the uploaded image file
    contents = await file.read()
    
    # Decode the image file into a numpy array
    image = face_recognition.load_image_file(contents)
    
    # Generate the face encodings
    face_encodings = face_recognition.face_encodings(image)
    
    # Check if exactly one face is found in the image
    if len(face_encodings) != 1:
        return {'message': 'No face found or multiple faces found'}
    
    # Store the face encodings and user details in the database
    database[face_encodings[0].tostring()] = {'name': name, 'email': email}
    
    return {'message': 'Registration successful'}

# Recognise endpoint
@app.post('/recognise/')
async def recognise(file: UploadFile):
    # Read the uploaded image file
    contents = await file.read()
    
    # Decode the image file into a numpy array
    image = face_recognition.load_image_file(contents)
    
    # Generate the face encodings
    face_encodings = face_recognition.face_encodings(image)
    
    # Check if exactly one face is found in the image
    if len(face_encodings) != 1:
        return {'message': 'No face found or multiple faces found'}
    
    # Look up the face encodings in the database
    for encoding in face_encodings:
        if encoding.tostring() in database:
            # Return the user details if a match is found
            return database[encoding.tostring()]
    
    return {'message': 'No match found'}

