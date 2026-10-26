# backend/app/api/routes/chatbot.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
import pandas as pd

from app.schemas.requests import ChatRequest
from app.core.database import get_db
from app.models.medicine import MedicineRecord
from app.ml.model_loader import chatbot_model, forecast_model

router = APIRouter()


@router.post("/chatbot")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    question_lower = req.text.lower()

    # --- Predict intent ---
    intent = "unknown"
    if chatbot_model is not None:
        try:
            intent = chatbot_model.predict([req.text])[0]
        except Exception:
            pass

    # --- Identify clinic and medicine mentioned in the question ---
    clinics = [c[0] for c in db.query(MedicineRecord.clinic).distinct().all()]
    medicines = [m[0] for m in db.query(MedicineRecord.medicine).distinct().all()]

    clinic = next((c for c in clinics if c.lower() in question_lower), None)
    medicine = next((m for m in medicines if m.lower() in question_lower), None)

    reply = (
        "I am a specialized assistant. I can only help with clinic stock, "
        "medicine expiry, and demand forecasts."
    )

    # --- Handle by intent ---
    if intent == "check_stock":
        if not clinic or not medicine:
            reply = "Please specify a clinic (e.g., Clinic A) and a medicine (e.g., ARVs)."
        else:
            total = db.query(func.sum(MedicineRecord.quantity_used)).filter(
                MedicineRecord.clinic == clinic,
                MedicineRecord.medicine == medicine
            ).scalar()
            if total:
                reply = f"{clinic} has historically used {int(total)} units of {medicine}."
            else:
                reply = "No matching record found for that clinic and medicine."

    elif intent == "check_expiry":
        today = date.today()
        expiry_limit = today + timedelta(days=30)

        query = db.query(MedicineRecord).filter(
            MedicineRecord.expiry_date >= today,
            MedicineRecord.expiry_date <= expiry_limit
        )
        if clinic:
            query = query.filter(MedicineRecord.clinic == clinic)

        expiring = query.all()

        if not expiring:
            reply = "No medicines are expiring within 30 days."
        else:
            items = [
                f"{row.medicine} ({row.stock_on_hand} units) at {row.clinic}"
                for row in expiring
            ]
            reply = "Expiring soon: " + ", ".join(sorted(set(items)))

    elif intent == "forecast_demand":
        if not clinic or not medicine:
            reply = "Please specify a clinic and medicine, e.g. 'Forecast for ARVs at Clinic A'."
        else:
            avg_usage = db.query(func.avg(MedicineRecord.quantity_used)).filter(
                MedicineRecord.clinic == clinic,
                MedicineRecord.medicine == medicine
            ).scalar()

            if avg_usage and forecast_model is not None:
                features = pd.DataFrame([{
                    "baseline_demand": avg_usage * 7,
                    "shelf_life": 78,
                    "seasonal_amplitude": 0.10
                }])
                try:
                    weekly_pred = float(forecast_model.predict(features)[0])
                    monthly_pred = int(round(weekly_pred * 4.3))
                    reply = (
                        f"AI forecast: {clinic} will need approximately "
                        f"{monthly_pred} units of {medicine} over the next 30 days."
                    )
                except Exception:
                    reply = f"Forecast unavailable for {clinic} and {medicine}."
            elif avg_usage:
                reply = (
                    f"Based on historical average, {clinic} will need about "
                    f"{int(avg_usage * 30)} units of {medicine} next month."
                )
            else:
                reply = "No historical data for that clinic and medicine."

    elif intent == "request_transfer":
        reply = "Transfer suggestions are not fully implemented in this prototype."

    elif intent == "detect_anomaly":
        reply = "Open the AI Insights panel on the dashboard to see detected anomalies."

    return {
        "user_message": req.text,
        "detected_intent": intent,
        "bot_reply": reply
    }