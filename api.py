from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import warnings
warnings.filterwarnings('ignore') # This hides the InconsistentVersionWarning

app = FastAPI(title="Water Potability API")

# 1. Load BOTH the Model and the Scaler
model = joblib.load('water.pkl')
scaler = joblib.load('scaler.pkl') 

class WaterData(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

@app.post("/predict")
def predict_water_quality(data: WaterData):
    # Convert user input into a DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # 2. SCALE THE DATA (This fixes the wrong predictions!)
    # It converts raw inputs like Solids=22014 into scaled numbers like 0.45
    scaled_input = scaler.transform(input_df)
    
    # 3. Predict using the scaled data
    prediction = model.predict(scaled_input)[0]
    
    if prediction == 1:
        result = "Potable (Safe to drink)"
    else:
        result = "Not Potable (Unsafe to drink)"
        
    return {"prediction": int(prediction), "status": result}