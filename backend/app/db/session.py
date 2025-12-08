from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import time

Base = declarative_base()

# Retry wrapper
def create_engine_with_retry(url, retries=10, delay=3):
    for i in range(retries):
        try:
            engine = create_engine(url, echo=False, future=True)
            # test connection
            conn = engine.connect()
            conn.close()
            print("Database connected successfully.")
            return engine
        except Exception as e:
            print(f"Database connection failed ({i+1}/{retries}). Retrying in {delay}s...")
            print("Error:", e)
            time.sleep(delay)
    raise Exception("Database connection could not be established after retries.")

engine = create_engine_with_retry(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
