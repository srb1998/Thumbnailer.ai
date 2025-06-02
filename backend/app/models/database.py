from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Supabase PostgreSQL connection
# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "postgresql://postgres:sourabhgr8@db.jyfrdylpgavkrlkmxzsg.supabase.co:5432/postgres"
# Format: postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Thumbnail(Base):
    __tablename__ = "thumbnails"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True, nullable=False)
    description = Column(Text)
    genre = Column(String(100), nullable=False)
    style = Column(String(100), default="modern")
    color_scheme = Column(String(100), default="vibrant")
    image_url = Column(String(1000), nullable=False)
    download_url = Column(String(1000))
    thumbnail_url = Column(String(1000))  # Smaller preview
    public_id = Column(String(200))  # Cloudinary ID
    prompt_used = Column(Text)
    user_email = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    download_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    generation_time = Column(Float)  # Track performance

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    total_thumbnails = Column(Integer, default=0)
    total_downloads = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    subscription_tier = Column(String(50), default="free")  # free, pro, etc.

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    thumbnail_id = Column(Integer, index=True)
    action = Column(String(50))  # 'generate', 'download', 'email'
    user_email = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    metadata_data = Column(Text)  # JSON string for additional data

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()