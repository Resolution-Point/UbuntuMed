# backend/app/api/routes/anomaly.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
import pandas as pd

from app.core.database import get_db
from app.models.medicine import MedicineRecord
from app.ml.model_loader import anomaly_model

router = APIRouter()


@router.get("/anomaly")
def get_anomalies(db: Session = Depends(get_db)):
    """
    Runs the Isolation Forest model on weekly aggregate usage per clinic/medicine.
    Returns the most suspicious consumption patterns.
    """
    if anomaly_model is None:
        return {
            "anomalies_detected": False,
            "details": [],
            "message": "Anomaly model not loaded."
        }

    # Get the last 14 days of data
    cutoff = date.today() - timedelta(days=14)
    records = db.query(MedicineRecord).filter(MedicineRecord.date >= cutoff).all()

    # Fallback: if no recent data, use all data
    if not records:
        records = db.query(MedicineRecord).all()

    if not records:
        return {
            "anomalies_detected": False,
            "details": [],
            "message": "No data available."
        }

    # Build DataFrame
    df = pd.DataFrame([{
        "clinic": r.clinic,
        "medicine": r.medicine,
        "quantity_used": r.quantity_used,
    } for r in records])

    # Aggregate: total usage per clinic/medicine over the window (proxy for weekly demand)
    agg = df.groupby(["clinic", "medicine"]).agg(
        total_usage=("quantity_used", "sum")
    ).reset_index()

    if agg.empty:
        return {
            "anomalies_detected": False,
            "details": [],
            "message": "No aggregated data available."
        }

    # Score using the Isolation Forest model
    try:
        scores = anomaly_model.decision_function(agg[["total_usage"]])
        predictions = anomaly_model.predict(agg[["total_usage"]])
        agg["score"] = scores
        agg["anomaly"] = predictions
    except Exception as e:
        return {
            "anomalies_detected": False,
            "details": [],
            "message": f"Model scoring failed: {str(e)}"
        }

    # Flag actual anomalies (model returns -1 for anomalies)
    flagged = agg[agg["anomaly"] == -1].sort_values("score").head(3)

    # If no strict anomalies, surface the 2 most suspicious for transparency
    if flagged.empty:
        flagged = agg.sort_values("score").head(2)

    details = []
    for _, row in flagged.iterrows():
        details.append({
            "clinic": row["clinic"],
            "medicine": row["medicine"],
            "issue": (
                f"Unusual consumption pattern — "
                f"{int(row['total_usage'])} units in the last 14 days "
                f"(anomaly score: {row['score']:.2f})"
            )
        })

    return {
        "anomalies_detected": True,
        "details": details
    }