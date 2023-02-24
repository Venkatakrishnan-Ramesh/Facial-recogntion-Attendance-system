from typing import Optional
import utils
from fastapi import FastAPI , File , UploadFile , Request

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello APP"}

@app.post("/predict")
async def predict(file:UploadFile = File(...)):
    print(file.file.read())
    return {"message": "Hello from predict"} 
