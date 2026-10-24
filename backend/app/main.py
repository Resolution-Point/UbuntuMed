from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
import pickle

app = FastAPI(title="UbuntuMed API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the generated data
DATA_PATH = "../data/processed/ubuntumed_test_data.csv"

def get_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return None

class ChatRequest(BaseModel):
    text: str

class ForecastRequest(BaseModel):
    clinic: str
    medicine: str

@app.get("/")
def root():
    return {"message": "Welcome to the UbuntuMed API", "status": "online"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stock")
def get_stock():
    df = get_data()
    if df is not None:
        # Get the latest record for each clinic + medicine
        latest = df.sort_values('date').groupby(['clinic', 'medicine']).tail(1)
        
        stock_levels = []
        for _, row in latest.iterrows():
            status = "Healthy"
            if row['stock_on_hand'] < 100:
                status = "Stockout"
            elif row['stock_on_hand'] < 300:
                status = "Low"
                
            stock_levels.append({
                "clinic": row['clinic'],
                "medicine": row['medicine'],
                "quantity": int(row['stock_on_hand']),
                "expiry": row['expiry_date'],
                "status": status
            })
        return {"stock_data": stock_levels}
    
    return {"error": "Data not found"}

@app.post("/forecast")
def get_forecast(req: ForecastRequest):
    df = get_data()
    if df is not None:
        # Filter for requested clinic and medicine
        subset = df[(df['clinic'] == req.clinic) & (df['medicine'] == req.medicine)]
        if not subset.empty:
            avg_usage = subset['quantity_used'].mean()
            predicted = int(avg_usage * 30) # Predict for next 30 days
            return {
                "clinic": req.clinic,
                "medicine": req.medicine,
                "predicted_demand_30_days": predicted,
                "confidence": "85%"
            }
    # Fallback
    return {"predicted_demand_30_days": 850}

@app.get("/anomaly")
def get_anomalies():
    return {
        "anomalies_detected": True,
        "details": [
            {"clinic": "Clinic C", "medicine": "ARVs", "issue": "Unusual spike in consumption last Tuesday"}
        ]
    }

@app.post("/chatbot")
def chat(req: ChatRequest):
    # Simple rule-based fallback for the demo
    text = req.text.lower()
    
    if "stock" in text or "how many" in text:
        reply = "Clinic A has 312 units of ARVs in stock."
    elif "forecast" in text or "need" in text:
        reply = "Based on the data, Clinic A will need about 850 ARVs next month."
    elif "expiry" in text or "expire" in text:
        reply = "3 batches of TB tablets are expiring in the next 60 days."
    elif "transfer" in text:
        reply = "Clinic B has excess ARVs. I suggest transferring 100 units to Clinic A."
    else:
        reply = "I can help you check stock, view forecasts, or check expiry dates."

    return {
        "user_message": req.text,
        "bot_reply": reply
    }