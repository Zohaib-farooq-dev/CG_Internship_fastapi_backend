from sqlalchemy import Column, Integer, String # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    No_of_doctors = Column(Integer, nullable = False)

