import os
import pickle

MODELS_DIR = "../ml_training/saved_models"

def load_model(filename):
    path = os.path.join(MODELS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

# Load all models once
forecast_model = load_model("forecast_model.pkl")
anomaly_model = load_model("anomaly_model.pkl")
chatbot_model = load_model("chatbot_nlp.pkl")