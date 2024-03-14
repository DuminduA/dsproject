from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


# Database settings.
engine = create_engine(f"postgresql://postgres:postgres@localhost:5433/salesdb?sslmode=require")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()