from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./my_doctor.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Specialty(Base):
    __tablename__ = "specialties"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g., "طب عام", "أسنان"
    icon_url = Column(String, nullable=True)
    
    doctors = relationship("Doctor", back_populates="specialty")

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    specialty_id = Column(Integer, ForeignKey("specialties.id"), nullable=False)
    phone = Column(String)
    email = Column(String)
    photo_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    specialty = relationship("Specialty", back_populates="doctors")
    clinics = relationship("Clinic", back_populates="doctor", cascade="all, delete-orphan")

class Clinic(Base):
    __tablename__ = "clinics"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    phone = Column(String)
    working_hours = Column(String)  # e.g., "8:00 AM - 4:00 PM"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    doctor = relationship("Doctor", back_populates="clinics")

# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
