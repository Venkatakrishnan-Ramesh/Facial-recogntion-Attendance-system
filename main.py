import io
import os
import face_recognition
from PIL import Image
from fastapi import FastAPI, File, Form, HTTPException

app = FastAPI()

@app.post("/register/")
async def register(name: str, email: str, image_file: bytes):
    try:
        image = face_recognition.load_image_file(io.BytesIO(image_file))
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) == 0:
            raise HTTPException(status_code=400, detail="No face found in image")
        elif len(face_encodings) > 1:
            raise HTTPException(status_code=400, detail="Multiple faces found in image")
        else:
            known_faces[name] = face_encodings[0]
            db[email] = name

        return JSONResponse(content={"message": "Registration successful"})
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Recognize endpoint
@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    # Read image file
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Find face location and encoding
    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    # Compare face encoding to dictionary of known faces
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([user['face_encoding'] for user in users.values()], face_encoding.tolist())
        if True in matches:
            index = matches.index(True)
            email = list(users.keys())[index]
            name = users[email]['name']
            return {"name": name}

    return {"name": "Unknown"}

