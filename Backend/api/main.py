from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Model from Local Folder
MODEL_PATH = os.path.join(os.path.dirname(__file__), "crop_recommendation_model_gb.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    raise RuntimeError(f"Error loading model: {str(e)}")

# Define Input Format
class CropPredictionRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float
    feature6: float
    feature7: float

# Root Route
@app.get("/")
def read_root():
    return {"message": "Crop Recommendation API is running!"}

# ✅ Prediction Route
@app.post("/predict")
def predict(request: CropPredictionRequest):
    try:
        # Convert input to numpy array
        features = np.array([
            request.feature1, 
            request.feature2, 
            request.feature3, 
            request.feature4, 
            request.feature5, 
            request.feature6, 
            request.feature7
        ]).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)

        return {"prediction": prediction[0]}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
