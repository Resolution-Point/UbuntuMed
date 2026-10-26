from fastapi import APIRouter
from app.schemas.requests import ChatRequest
from app.services.data_service import get_data
from app.ml.model_loader import chatbot_model
from datetime import date, timedelta
import pandas as pd

router = APIRouter()

@router.post("/chatbot")
def chat(req: ChatRequest):
    df = get_data()
    if df is None: return {"bot_reply": "Database not connected."}

    question_lower = req.text.lower()
    
    # Predict Intent
    intent = "unknown"
    if chatbot_model:
        try: intent = chatbot_model.predict([req.text])[0]
        except Exception: pass

    # Find Clinic & Medicine
    clinics = sorted(df["clinic"].dropna().unique(), key=len, reverse=True)
    clinic = next((c for c in clinics if c.lower() in question_lower), None)
    medicines = sorted(df["medicine"].dropna().unique(), key=len, reverse=True)
    medicine = next((m for m in medicines if m.lower() in question_lower), None)

    reply = "I am a specialized assistant. I can only help you with clinic stock, medicine expiry, and demand forecasts."

    if intent == "check_stock":
        if not clinic or not medicine:
            reply = "Please specify a clinic (e.g., Clinic A) and a medicine (e.g., ARVs)."
        else:
            result = df[(df["clinic"] == clinic) & (df["medicine"].str.lower() == medicine.lower())]
            if not result.empty:
                quantity = result["quantity_used"].sum() 
                reply = f"{clinic} has {quantity} units of {medicine} available."

    elif intent == "check_expiry":
        records = df.copy()
        records["expiry_date"] = pd.to_datetime(records["expiry_date"], errors="coerce").dt.date
        if clinic: records = records[records["clinic"] == clinic]
        
        today = date.today()
        expiring = records[records["expiry_date"].notna() & (records["expiry_date"] >= today) & (records["expiry_date"] <= today + timedelta(days=30))]
        
        if expiring.empty: reply = "No medicines are expiring within 30 days."
        else:
            items = [f"{row['medicine']} ({row['quantity_used']} units) at {row['clinic']}" for _, row in expiring.iterrows()]
            reply = "Expiring soon: " + ", ".join(items)

    return {"user_message": req.text, "detected_intent": intent, "bot_reply": reply}