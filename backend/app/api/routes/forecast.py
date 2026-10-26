from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.requests import ForecastRequest
from app.core.database import get_db
from app.models.medicine import MedicineRecord
from sqlalchemy import func

router = APIRouter()

@router.post("/forecast")
def get_forecast(req: ForecastRequest, db: Session = Depends(get_db)):
    avg_usage = db.query(func.avg(MedicineRecord.quantity_used)).filter(
        MedicineRecord.clinic == req.clinic,
        MedicineRecord.medicine == req.medicine
    ).scalar()
    
    if avg_usage:
        predicted = int(avg_usage * 30) # predict for 30 days
        return {"clinic": req.clinic, "medicine": req.medicine, "predicted_demand_30_days": predicted}
        
    return {"predicted_demand_30_days": 850}