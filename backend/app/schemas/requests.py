from pydantic import BaseModel

class ChatRequest(BaseModel):
    text: str

class ForecastRequest(BaseModel):
    clinic: str
    medicine: str
    days: int = 30