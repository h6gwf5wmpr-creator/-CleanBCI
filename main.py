from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI()
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

class EEGInput(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: EEGInput):
    X = np.array(data.features).reshape(1, -1)
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)
    label = "Right Hand" if int(pred[0]) == 1 else "Left Hand"
    return {"prediction": int(pred[0]), "label": label}
