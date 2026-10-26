import pandas as pd
import os

DATA_PATH = "../data/processed/ubuntumed_test_data.csv"

def get_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return None