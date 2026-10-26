from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.medicine import MedicineRecord
from sqlalchemy import func

router = APIRouter()

@router.get("/stock")
def get_stock(db: Session = Depends(get_db)):
    # Get the latest record per clinic/medicine
    # We use a subquery to find the max date for each clinic/medicine combo
    subq = db.query(
        MedicineRecord.clinic,
        MedicineRecord.medicine,
        func.max(MedicineRecord.date).label('max_date')
    ).group_by(MedicineRecord.clinic, MedicineRecord.medicine).subquery()

    latest_records = db.query(MedicineRecord).join(
        subq,
        (MedicineRecord.clinic == subq.c.clinic) &
        (MedicineRecord.medicine == subq.c.medicine) &
        (MedicineRecord.date == subq.c.max_date)
    ).all()

    stock_levels = []
    for row in latest_records:
        status = "Healthy"
        if row.stock_on_hand < 100: status = "Stockout"
        elif row.stock_on_hand < 300: status = "Low"
        
        stock_levels.append({
            "clinic": row.clinic,
            "medicine": row.medicine,
            "quantity": row.stock_on_hand,
            "expiry": str(row.expiry_date),
            "status": status
        })
        
    return {"stock_data": stock_levels}