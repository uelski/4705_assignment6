import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import json
from datetime import datetime

# create app
app = FastAPI(
    title="Movie Review Sentiment Analysis",
)

# load model
try:
    model = joblib.load("sentiment_model.pkl")
except FileNotFoundError:
    print("Model file not found")
    model = None

# create prediction request model
class PredictionRequest(BaseModel):
    text: str
    true_label: str

# generate startup event
@app.on_event("startup")
def startup_event():
    """
    Startup event to print if model is loaded or not
    """
    if model is None:
        print("Warning: Model not loaded")
    else:
        print("Model loaded successfully")

# get health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify if the API is running
    """
    if model is None:
        return {"status": "unhealthy", "message": "Model not loaded but app is running"}
    return {"status": "healthy", "message": "Model loaded successfully and app is running"}

# create predict endpoint
@app.post("/predict")
def predict(request: PredictionRequest):
    """
    Predict endpoint to predict the sentiment of the provided review text.
    Returns a JSON object with the predicted sentiment, "positive" or "negative"
    """
    # check if model is loaded  
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded")
    
    # predict sentiment
    try:
        prediction = model.predict([request.text])
        
        # create log entry
        log = {
            "timestamp": datetime.now().isoformat(),
            "request_text": request.text,
            "predicted_sentiment": prediction[0],
            "true_sentiment": request.true_label
        }

        # write log entry
        with open("/logs/prediction_logs.json", "a") as f:
            f.write(json.dumps(log) + "\n")

        # return prediction
        return {"sentiment": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error predicting sentiment: {e}")
