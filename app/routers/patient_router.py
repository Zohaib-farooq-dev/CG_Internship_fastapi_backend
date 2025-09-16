from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from app.schemas.patients import Patient, PatientUpdate   #  create ke liye alag schema
from app.services import patient_service
from app.core.database import get_db  # DB dependency

router = APIRouter()

@router.get("/")
def hello():
    return {"message": "Patient Management System API"}

@router.get("/about")
def about():
    return {"message": "Fully functional API for managing your patients"}

@router.get("/view")
def view(db: Session = Depends(get_db)):   # 👈 DB session inject
    return patient_service.view(db)

@router.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient", example="P001"),
    db: Session = Depends(get_db)
):
    return patient_service.view_patient(db, patient_id)

@router.get("/sort")
def sorted_patients(
    sort_by: str = Query("weight", description="Sort by weight, height or bmi"),
    order: str = Query("asc", description="asc or desc"),
    db: Session = Depends(get_db)
):
    return patient_service.sorted_patients(db, sort_by, order)

@router.post("/create")
def create(patient: Patient, db: Session = Depends(get_db)):
    return patient_service.create_patient(db, patient)

@router.put("/edit/{patient_id}")
def update(
    patient_id: str,
    patient: PatientUpdate,
    db: Session = Depends(get_db)
):
    return patient_service.update_patient(db, patient_id, patient)

@router.delete("/delete/{patient_id}")
def delete(patient_id: str, db: Session = Depends(get_db)):
    return patient_service.patient_delete(db, patient_id)
