from fastapi import APIRouter
from app.schemas.requests import ForecastRequest
from app.services.data_service import get_data

router = APIRouter()

@router.post("/forecast")
def get_forecast(req: ForecastRequest):
    df = get_data()
    if df is not None:
        subset = df[(df['clinic'] == req.clinic) & (df['medicine'] == req.medicine)]
        if not subset.empty:
            avg_usage = subset['quantity_used'].mean()
            predicted = int(avg_usage * 30)
            return {"clinic": req.clinic, "medicine": req.medicine, "predicted_demand_30_days": predicted}
    return {"predicted_demand_30_days": 850}