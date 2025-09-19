"""
Pydantic models for patient data validation and API I/O schemas.

This module defines:
- Patient: Full patient schema with validation, example values, and computed fields 
  (BMI and health verdict) derived automatically from height and weight.
- PatientUpdate: Partial schema for updating existing patient records with optional fields.

These models ensure strict type checking, input validation, and automatic 
calculation of derived attributes when used in FastAPI endpoints.
"""
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class PatientBase(BaseModel):
    id: Annotated[str,Field(...,description='Id of the patient',example='P001')]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City where the patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the patient')]
    gender:Annotated[Literal['male','female','other'],Field(...,description='Gender of teh patient')]
    height:Annotated[float,Field(...,description='Heightof teh patient in meters')]
    weight:Annotated[float,Field(...,description='Weight of  the patient in Kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<28:
            return 'Normal'
        else:
            return 'Obese'
        

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    doctor_id: int

    class Config:
        from_attributes = True   

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    doctor_id: Annotated[Optional[int], Field(default=None,gt =0)]