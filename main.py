from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

class EEGInput(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: EEGInput):
    input_features = list(data.features)
    
    # الحل الجذري: مطابقة حجم البيانات مع ما يتوقعه الـ Scaler (64 ميزة)
    if len(input_features) < 64:
        input_features = input_features + [0.0] * (64 - len(input_features))
    elif len(input_features) > 64:
        input_features = input_features[:64]
        
    X = np.array([input_features])
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)
    label = "Right Hand" if int(pred[0]) == 1 else "Left Hand"
    return {"prediction": int(pred[0]), "label": label}
