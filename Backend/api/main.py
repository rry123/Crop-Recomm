from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory of the current file (useful for relative paths)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the trained Gradient Boosting model using a relative path
model_path = os.path.join(BASE_DIR, "crop_recommendation_model_gb.pkl")

try:
    model = joblib.load(model_path)
except Exception as e:
    raise RuntimeError(f"Error loading the model: {str(e)}")

# Define input format using Pydantic (individual features)
class CropPredictionRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float
    feature6: float
    feature7: float

# Root route to check if API is running
@app.get("/")
def read_root():
    return {"message": "Crop Recommendation API is up and running!"}

# Prediction endpoint
@app.post("/predict")
def predict(request: CropPredictionRequest):
    try:
        # Extract the features and convert them to a numpy array
        features = np.array([
            request.feature1, 
            request.feature2, 
            request.feature3, 
            request.feature4, 
            request.feature5, 
            request.feature6, 
            request.feature7
        ]).reshape(1, -1)  # Reshape to match model input
        
        # Make the prediction
        prediction = model.predict(features)
        
        # Return the prediction result
        return {"prediction": prediction[0]}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
