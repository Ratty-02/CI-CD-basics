import joblib
import os

from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator

PORT = int(os.getenv("PORT", "8000"))

# Create the FastAPI application
app = FastAPI()

# Configure Prometheus monitoring
Instrumentator().instrument(app).expose(app)


# Define input features
class PredictionRequest(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


# Load the trained model once
model = joblib.load("iris_model.joblib")


# Health endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}


# Prediction endpoint
@app.post("/predict")
def predict(data: PredictionRequest):

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = model.predict(features)

    return {"prediction": int(prediction[0])}