from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, stock, forecast, chatbot
from app.core.database import engine, Base

# Imports models so SQLAlchemy knows what tables to create
from app.models import medicine

# Creates the database tables if they don't exist
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

# Include all routes
app.include_router(health.router, tags=["System"])
app.include_router(stock.router, tags=["Inventory"])
app.include_router(forecast.router, tags=["AI Predictions"])
app.include_router(chatbot.router, tags=["AI Chatbot"])