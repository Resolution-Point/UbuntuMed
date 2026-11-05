from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.medicine import MedicineRecord

router = APIRouter()


@router.get("/redistribute")
def get_redistribution_suggestions(db: Session = Depends(get_db)):
    """Suggest moving excess or soon-to-expire medicine to clinics with low stock."""
    today = date.today()
    expiry_threshold = today + timedelta(days=90)

    latest_dates = db.query(
        MedicineRecord.clinic,
        MedicineRecord.medicine,
        func.max(MedicineRecord.date).label("max_date"),
    ).group_by(
        MedicineRecord.clinic,
        MedicineRecord.medicine,
    ).subquery()

    latest_records = db.query(MedicineRecord).join(
        latest_dates,
        (MedicineRecord.clinic == latest_dates.c.clinic)
        & (MedicineRecord.medicine == latest_dates.c.medicine)
        & (MedicineRecord.date == latest_dates.c.max_date),
    ).all()

    records_by_medicine = {}
    for record in latest_records:
        records_by_medicine.setdefault(record.medicine, []).append(record)

    suggestions = []
    for medicine, records in records_by_medicine.items():
        sources = [
            record
            for record in records
            if record.stock_on_hand is not None
            and record.stock_on_hand > 0
            and (record.expiry_date is None or record.expiry_date >= today)
            and (
                record.stock_on_hand > 500
                or (
                    record.expiry_date is not None
                    and today <= record.expiry_date <= expiry_threshold
                )
            )
        ]
        targets = [
            record
            for record in records
            if record.stock_on_hand is not None and record.stock_on_hand < 150
            and (record.expiry_date is None or record.expiry_date >= today)
        ]

        for source in sources:
            for target in targets:
                if source.clinic == target.clinic:
                    continue

                transfer_quantity = min(int(source.stock_on_hand * 0.5), 200)
                if transfer_quantity <= 0:
                    continue

                reason = "Overstocked"
                if source.expiry_date and today <= source.expiry_date <= expiry_threshold:
                    reason = f"Expiring on {source.expiry_date}"

                suggestions.append({
                    "medicine": medicine,
                    "from_clinic": source.clinic,
                    "to_clinic": target.clinic,
                    "transfer_quantity": transfer_quantity,
                    "reason": reason,
                })
                break

    return {"total_suggestions": len(suggestions), "suggestions": suggestions}
