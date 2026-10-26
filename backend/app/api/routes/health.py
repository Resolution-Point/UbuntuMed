from fastapi import APIRouter
from app.ml.model_loader import forecast_model, anomaly_model, chatbot_model

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "forecast_model_loaded": forecast_model is not None,
        "anomaly_model_loaded": anomaly_model is not None,
        "chatbot_model_loaded": chatbot_model is not None,
    }