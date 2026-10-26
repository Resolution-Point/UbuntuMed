# backend/app/models/medicine.py
from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class MedicineRecord(Base):
    __tablename__ = "medicine_inventory"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    clinic = Column(String, index=True)
    medicine = Column(String, index=True)
    quantity_used = Column(Integer)
    stock_on_hand = Column(Integer)
    expiry_date = Column(Date)