from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from app.schemas.patients import Patient, PatientUpdate   #  create ke liye alag schema
from app.services import patient_service
from app.core.database import get_db  # DB dependency

router = APIRouter()

@router.get("/")
def hello():
    """
    Endpoint: GET /
    Returns a welcome message for the Patient Management API.
    """
    return {"message": "Patient Management System API"}

@router.get("/about")
def about():
    """
    Endpoint: GET /about
    Returns basic information about the API.
    """
    return {"message": "Fully functional API for managing your patients"}

@router.get("/view")
def view(db: Session = Depends(get_db)):   # DB session inject
    """
    Endpoint: GET /view
    Fetches all patients from the database by calling the service layer.
    
    Args:
        db (Session): Database session injected via dependency.
    """
    return patient_service.view(db)

@router.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient", example="P001"),
    db: Session = Depends(get_db)
):
    """
    Endpoint: GET /patient/{patient_id}
    Recieves a single patient by ID and passes the query to the service layer.

    Args:
        patient_id (str): Unique ID of the patient.
        db (Session): Database session.
    """
    return patient_service.view_patient(db, patient_id)

@router.get("/sort")
def sorted_patients(
    sort_by: str = Query("weight", description="Sort by weight, height or bmi"),
    order: str = Query("asc", description="asc or desc"),
    db: Session = Depends(get_db)
):
    """
    Endpoint: GET /sort
    Returns patients sorted by the specified field and order.

    Args:
        sort_by (str): Field to sort by (weight, height, bmi).
        order (str): Sort order (asc or desc).
        db (Session): Database session.
    """
    return patient_service.sorted_patients(db, sort_by, order)

@router.post("/create",status_code = status.HTTP_201_CREATED)
def create(patient: Patient, db: Session = Depends(get_db)):
    """
    Endpoint: POST /create
    Receives follwoing arguments and pass them to create_patient() method in service layer.

    Args:
        patient (Patient): Pydantic model containing patient data.
        db (Session): Database session.
    """
    return patient_service.create_patient(db, patient)

@router.put("/edit/{patient_id}",status_code=status.HTTP_204_NO_CONTENT)
def update(
    patient_id: str,
    patient: PatientUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint: PUT /edit/{patient_id}
    Receives follwoing arguments and pass them to update_patient() method in service layer.

    Args:
        patient_id (str): ID of the patient to update.
        patient (PatientUpdate): Partial patient update data.
        db (Session): Database session.
    """
    return patient_service.update_patient(db, patient_id, patient)

@router.delete("/delete/{patient_id}")
def delete(patient_id: str, db: Session = Depends(get_db)):
    """
    Endpoint: DELETE /delete/{patient_id}
    Receives follwoing arguments and pass them to patient_delete() method in service layer.

    Args:
        patient_id (str): ID of the patient to delete.
        db (Session): Database session.
    """
    return patient_service.patient_delete(db, patient_id)
