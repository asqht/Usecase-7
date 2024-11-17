from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load the saved model and scaler (if used)

model = joblib.load('KMeans.joblib')
scaler = joblib.load('scaler.joblib')

# GET request
@app.get("/")
def read_root():
    return {"message": "Welcome to the Football Player Model API"}

# Define Pydantic model for input data validation
class InputFeatures(BaseModel):
    
    appearance: int
    minutes_played : int

# Preprocessing function for scaling if necessary
def preprocess(input_features: InputFeatures):
    # Convert input data to a DataFrame
    df = pd.DataFrame([input_features.dict()])
    # Uncomment if using a scaler, otherwise skip this line
    # df = scaler.transform(df)
    return df

# Prediction endpoint
@app.post("/predict")
async def predict(input_features: InputFeatures):
    # Preprocess data
    data = preprocess(input_features)
    # Make prediction
    y_pred = model.predict(data)
    return {"prediction": y_pred.tolist()[0]}
