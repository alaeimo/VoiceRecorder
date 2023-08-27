from sqlalchemy import create_engine, Column, Integer, String, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_URL
from datetime import datetime

Base = declarative_base()

class RecordingFile(Base):
    __tablename__ = 'recording_files'

    id = Column(Integer, primary_key=True)
    file_name = Column(String, unique=True)
    file_path = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
