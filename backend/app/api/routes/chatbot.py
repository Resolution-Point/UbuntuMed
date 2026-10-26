from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.requests import ChatRequest
from app.core.database import get_db
from app.models.medicine import MedicineRecord
from app.ml.model_loader import chatbot_model
from datetime import date, timedelta
from sqlalchemy import func

router = APIRouter()

@router.post("/chatbot")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    question_lower = req.text.lower()
    
    intent = "unknown"
    if chatbot_model:
        try: intent = chatbot_model.predict([req.text])[0]
        except Exception: pass

    # Get unique clinics and meds from DB
    clinics = [c[0] for c in db.query(MedicineRecord.clinic).distinct().all()]
    medicines = [m[0] for m in db.query(MedicineRecord.medicine).distinct().all()]
    
    clinic = next((c for c in clinics if c.lower() in question_lower), None)
    medicine = next((m for m in medicines if m.lower() in question_lower), None)

    reply = "I am a specialized assistant. I can help with stock, expiry, and forecasts."

    if intent == "check_stock":
        if not clinic or not medicine:
            reply = "Please specify a clinic and a medicine."
        else:
            result = db.query(func.sum(MedicineRecord.quantity_used)).filter(
                MedicineRecord.clinic == clinic,
                MedicineRecord.medicine == medicine
            ).scalar()
            
            if result:
                reply = f"{clinic} has historically used {result} units of {medicine}."
            else:
                reply = "No matching stock record found."

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
            items = [f"{row.medicine} ({row.stock_on_hand} units) at {row.clinic}" for row in expiring]
            reply = "Expiring soon: " + ", ".join(set(items))

    return {"user_message": req.text, "detected_intent": intent, "bot_reply": reply}