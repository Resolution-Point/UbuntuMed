
import pandas as pd
from sqlalchemy import create_engine


SUPABASE_URL = "postgresql+psycopg2://postgres.yqgtjibhfniswxezpoja:4Rhw82WazFEeXcP4@aws-0-eu-west-1.pooler.supabase.com:5432/postgres"

engine = create_engine(SUPABASE_URL)

print("Reading CSV...")
df = pd.read_csv("data/processed/ubuntumed_test_data.csv")


df.insert(0, 'id', range(1, len(df) + 1))


df['date'] = pd.to_datetime(df['date']).dt.date
df['expiry_date'] = pd.to_datetime(df['expiry_date']).dt.date

print("Uploading to Supabase (this might take a few seconds)...")

df.to_sql("medicine_inventory", engine, if_exists="replace", index=False)

print(" Data migration complete! You can now test /stock")