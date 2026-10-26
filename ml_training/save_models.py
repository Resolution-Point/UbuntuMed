"""
One-time script to train and save all ML models as .pkl files.
Run from project root: python ml_training/save_models.py
Or from ml_training/: python save_models.py
"""
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, IsolationForest

# Paths — script lives in ml_training/, so go up 1 level to reach project root
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
SAVED_MODELS_DIR = SCRIPT_DIR / "saved_models"
CHATBOT_DATA = PROJECT_ROOT / "ChatBot" / "ubuntumed_chatbot_training_dataset.csv"

print(f"Script dir: {SCRIPT_DIR}")
print(f"Project root: {PROJECT_ROOT}")
print(f"Looking for chatbot data: {CHATBOT_DATA}")
print()

if not CHATBOT_DATA.exists():
    raise FileNotFoundError(f"Chatbot training data not found at {CHATBOT_DATA}")

SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# 1. CHATBOT MODEL
# ============================================
print("Training chatbot model...")
chat_data = pd.read_csv(CHATBOT_DATA)
print(f"  Loaded {len(chat_data)} training questions")

chatbot = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])
chatbot.fit(chat_data["text"], chat_data["intent"])

with open(SAVED_MODELS_DIR / "chatbot_nlp.pkl", "wb") as f:
    pickle.dump(chatbot, f)
print("   Saved chatbot_nlp.pkl")

# ============================================
# 2. FORECAST MODEL
# ============================================
print("Training forecast model...")
np.random.seed(42)
drugs = pd.DataFrame({
    "drug_id": ["D01","D02","D03","D04","D05","D06","D07","D08","D09","D10",
                "D11","D12","D13","D14","D15","D16","D17","D18","D19"],
    "baseline_demand": [320,90,210,240,180,70,130,450,300,40,
                        260,170,200,85,55,75,140,190,230],
    "shelf_life": [104,52,104,104,104,78,104,104,78,52,
                   78,78,104,78,52,78,78,104,78],
    "seasonal_amplitude": [0.05,0.05,0.04,0.04,0.04,0.03,0.03,0.25,0.30,0.20,
                           0.15,0.12,0.25,0.30,0.35,0.30,0.25,0.10,0.30]
})
drugs["weekly_demand"] = drugs["baseline_demand"] * (
    1 + np.random.uniform(-0.15, 0.15, len(drugs))
)

X = drugs[["baseline_demand", "shelf_life", "seasonal_amplitude"]]
y = drugs["weekly_demand"]
forecast_model = RandomForestRegressor(n_estimators=100, random_state=42)
forecast_model.fit(X, y)

with open(SAVED_MODELS_DIR / "forecast_model.pkl", "wb") as f:
    pickle.dump(forecast_model, f)
print("   Saved forecast_model.pkl")

# ============================================
# 3. ANOMALY MODEL
# ============================================
print("Training anomaly model...")
iso = IsolationForest(contamination=0.1, random_state=42)
iso.fit(drugs[["weekly_demand"]])

with open(SAVED_MODELS_DIR / "anomaly_model.pkl", "wb") as f:
    pickle.dump(iso, f)
print("   Saved anomaly_model.pkl")

print(f"\n All models saved to: {SAVED_MODELS_DIR}")