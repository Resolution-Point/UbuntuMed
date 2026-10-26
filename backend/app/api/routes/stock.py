from fastapi import APIRouter
from app.services.data_service import get_data

router = APIRouter()

@router.get("/stock")
def get_stock():
    df = get_data()
    if df is not None:
        latest = df.sort_values('date').groupby(['clinic', 'medicine']).tail(1)
        stock_levels = []
        for _, row in latest.iterrows():
            status = "Healthy"
            if row['stock_on_hand'] < 100: status = "Stockout"
            elif row['stock_on_hand'] < 300: status = "Low"
            stock_levels.append({
                "clinic": row['clinic'],
                "medicine": row['medicine'],
                "quantity": int(row['stock_on_hand']),
                "expiry": row['expiry_date'],
                "status": status
            })
        return {"stock_data": stock_levels}
    return {"error": "Data not found"}