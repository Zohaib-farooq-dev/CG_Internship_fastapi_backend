"""
Pydantic models for doctors data validation and API I/O schemas.

This module defines:
- DoctorBase: Full doctor schema with validation, and field validator.
- DoctorCreate: Schema for creating doctor records.
- DoctorLogin: Schema for login doctor
- DoctorResponse: Schema for response which tells the API to in which form to response.

These models ensure strict type checking, input validation, and automatic 
calculation of derived attributes when used in FastAPI endpoints.
"""
from pydantic import BaseModel, EmailStr, field_validator
from .patients import PatientBase
from typing import List

class DoctorBase(BaseModel):
    name: str
    email: EmailStr

    # Name should not contain digits
    @field_validator('name')
    @classmethod
    def name_must_be_alpha(cls, v: str) -> str:
        if any(char.isdigit() for char in v):
            raise ValueError('Name cannot contain numbers')
        return v

class DoctorCreate(DoctorBase):
    password: str  # plain password for creation

class DoctorLogin(BaseModel):
    username: EmailStr
    password: str 

class DoctorResponse(DoctorBase):
    id: int
    patients: List[PatientBase] = []
    class Config:
        orm_mode = True
