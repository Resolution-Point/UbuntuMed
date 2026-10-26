import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PASTE YOUR REAL URL HERE (Notice the +psycopg2:// and the //)
LOCAL_FALLBACK_URL = "postgresql+psycopg2://postgres.yqgtjibhfniswxezpoja:4Rhw82WazFEeXcP4@aws-0-eu-west-1.pooler.supabase.com:5432/postgres"

DATABASE_URL = os.getenv("DATABASE_URL", LOCAL_FALLBACK_URL)

# If Render gives us a URL starting with postgres://, fix it for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()