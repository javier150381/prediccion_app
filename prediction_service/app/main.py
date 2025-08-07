import os
from typing import List

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from tensorflow.keras.models import load_model

app = FastAPI()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")
model = load_model(MODEL_PATH)


class RainfallInput(BaseModel):
    precipitation: List[float]

    @validator("precipitation")
    def validate_precipitation(cls, v: List[float]) -> List[float]:
        if not v:
            raise ValueError("Input data cannot be empty")
        return v


@app.post("/predict")
def predict(data: RainfallInput):
    try:
        arr = np.array(data.precipitation, dtype=float)
    except ValueError:
        raise HTTPException(status_code=400, detail="Precipitation values must be floats")

    if arr.size == 0:
        raise HTTPException(status_code=400, detail="Input data cannot be empty")

    min_val = arr.min()
    range_val = arr.max() - min_val
    if range_val != 0:
        arr = (arr - min_val) / range_val

    arr = arr.reshape(1, arr.shape[0], 1)
    try:
        prediction = model.predict(arr)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {"prediction": prediction.tolist()}
