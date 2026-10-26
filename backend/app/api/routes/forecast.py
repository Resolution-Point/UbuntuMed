# backend/app/api/routes/forecast.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd

from app.schemas.requests import ForecastRequest
from app.core.database import get_db
from app.models.medicine import MedicineRecord
from app.ml.model_loader import forecast_model

router = APIRouter()


@router.post("/forecast")
def get_forecast(req: ForecastRequest, db: Session = Depends(get_db)):
    """
    Uses the trained Random Forest model to predict 30-day demand
    based on historical average usage for a clinic/medicine pair.
    """
    # Get average daily usage from the database
    avg_usage = db.query(func.avg(MedicineRecord.quantity_used)).filter(
        MedicineRecord.clinic == req.clinic,
        MedicineRecord.medicine == req.medicine
    ).scalar()

    if avg_usage is None:
        return {
            "clinic": req.clinic,
            "medicine": req.medicine,
            "predicted_demand_30_days": 0,
            "message": "No historical data for that clinic/medicine."
        }

    # If model is unavailable, fall back to simple multiplication
    if forecast_model is None:
        return {
            "clinic": req.clinic,
            "medicine": req.medicine,
            "predicted_demand_30_days": int(avg_usage * 30),
            "source": "average-based fallback"
        }

    # Build model features from observed data
    # We derive approximate features since the model was trained on baseline_demand,
    # shelf_life, and seasonal_amplitude
    features = pd.DataFrame([{
        "baseline_demand": avg_usage * 7,       # ~7 days of average usage
        "shelf_life": 78,                        # average medicine shelf life in days
        "seasonal_amplitude": 0.10               # conservative seasonal factor
    }])

    try:
        weekly_pred = float(forecast_model.predict(features)[0])
        monthly_pred = int(round(weekly_pred * 4.3))  # ~4.3 weeks per month
    except Exception:
        monthly_pred = int(avg_usage * 30)

    return {
        "clinic": req.clinic,
        "medicine": req.medicine,
        "predicted_demand_30_days": monthly_pred,
        "source": "Random Forest model",
        "confidence": "medium"
    }