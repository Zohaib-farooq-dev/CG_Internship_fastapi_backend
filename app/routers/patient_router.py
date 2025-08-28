from fastapi import APIRouter, Path, Query
from app.models.patients import Patient, PatientUpdate
from app.services import patient_service

router = APIRouter()


@router.get("/")
def hello():
    return {"message": "Patient Management System API"}


@router.get("/about")
def about():
    return {"message": "Fully functional API for managing your patients"}


@router.get("/view")
def view():
    return patient_service.view()


@router.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient", example="P001")):
    return patient_service.view_patient(patient_id)


@router.get("/sort")
def sorted_patients(
    sort_by: str = Query("weight", description="Sort by weight, height or bmi"),
    order: str = Query("asc", description="asc or desc")
):
    return patient_service.sorted_patients(sort_by, order)


@router.post("/create")
def create(patient: Patient):
    return patient_service.create_patient(patient)


@router.put("/edit/{patient_id}")
def update(patient_id: str, patient: PatientUpdate):
    return patient_service.update_patient(patient_id, patient)


@router.delete("/delete/{patient_id}")
def delete(patient_id: str):
    return patient_service.patient_delete(patient_id)
