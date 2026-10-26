# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, stock, forecast, chatbot, anomaly
from app.core.database import engine, Base
from app.models import medicine  # noqa: F401 — registers models

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="UbuntuMed API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the UbuntuMed API", "status": "online"}


app.include_router(health.router, tags=["System"])
app.include_router(stock.router, tags=["Inventory"])
app.include_router(forecast.router, tags=["AI Predictions"])
app.include_router(anomaly.router, tags=["AI Predictions"])
app.include_router(chatbot.router, tags=["AI Chatbot"])