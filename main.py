from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello APP"}

@app.get("/predict")
def predict():
    return {"message": "Hello APP"}