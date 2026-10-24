import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Setup
os.makedirs('data/processed', exist_ok=True)
random.seed(42)
np.random.seed(42)

clinics = ["Clinic A", "Clinic B", "Clinic C", "Clinic D"]
medicines = ["ARVs", "TB Tablets", "Blood Pressure Meds", "Diabetes Meds"]
start_date = datetime.now() - timedelta(days=90)

data = []

for clinic in clinics:
    for med in medicines:
        base_usage = random.randint(50, 200)
        current_stock = random.randint(100, 1000)
        # Expiry dates: some soon (near expiry), some later
        expiry_date = datetime.now() + timedelta(days=random.randint(10, 180))
        
        for day in range(90):
            date = start_date + timedelta(days=day)
            
            # Add some weekly seasonality (more usage on weekdays)
            if date.weekday() < 5:
                usage = int(np.random.normal(base_usage, 15))
            else:
                usage = int(np.random.normal(base_usage * 0.5, 10))
                
            # Ensure usage is positive
            usage = max(0, usage)
            
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "clinic": clinic,
                "medicine": med,
                "quantity_used": usage,
                "stock_on_hand": current_stock,
                "expiry_date": expiry_date.strftime("%Y-%m-%d")
            })

df = pd.DataFrame(data)
df.to_csv("data/processed/ubuntumed_test_data.csv", index=False)
print(f"Generated {len(df)} rows of test data and saved to data/processed/ubuntumed_test_data.csv")
