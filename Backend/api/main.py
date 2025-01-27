from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
# Load the trained Gradient Boosting model
model = joblib.load(r"F:\Btechproject2/Backend/Model/crop_recommendation_model_gb.pkl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input format using Pydantic (individual features)
class CropPredictionRequest(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float
    feature6: float
    feature7: float

@app.post("/predict")
def predict(request: CropPredictionRequest):
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
