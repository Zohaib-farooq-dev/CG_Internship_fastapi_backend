from sqlalchemy import Column, Integer, String, ForeignKey # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import relationship  # type: ignore
from app.core.database import Base

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    patients = relationship("Patient", back_populates="doctor")
