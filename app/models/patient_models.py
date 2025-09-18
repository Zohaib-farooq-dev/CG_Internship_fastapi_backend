"""
Database models for patient records.

Defines the Patient ORM model representing the 'patients' table,
including columns for personal info, physical measurements, and BMI verdict.
"""
from sqlalchemy import Column, String, Integer, Float, Enum
from app.core.database import Base
import enum

# Optional: Gender Enum for DB safety
class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    height = Column(Float, nullable=False)   # meters
    weight = Column(Float, nullable=False)   # kgs
    bmi = Column(Float, nullable=True)
    verdict = Column(String, nullable=True)
