import os
import pickle

# Path: backend/app/ml/model_loader.py
# up 1: ml/  up 2: app/  up 3: backend/  up 4: project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODELS_DIR = os.path.join(BASE_DIR, "ml_training", "saved_models")

def load_model(filename):
    path = os.path.join(MODELS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

forecast_model = load_model("forecast_model.pkl")
anomaly_model = load_model("anomaly_model.pkl")
chatbot_model = load_model("chatbot_nlp.pkl")