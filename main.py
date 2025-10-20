from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Healthcare AI Model Service")

Instrumentator().instrument(app).expose(app)

class PredictionRequest(BaseModel):
    patient_data: dict

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    model_version: str = "v1.0.0"

@app.get("/")
async def read_root():
    return {"message": "Healthcare AI Model Service is running."}

@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(request: PredictionRequest):
    if request.patient_data.get("age", 0) > 60:
        return PredictionResponse(prediction="High Risk", confidence=0.92)
    else:
        return PredictionResponse(prediction="Low Risk", confidence=0.75)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
