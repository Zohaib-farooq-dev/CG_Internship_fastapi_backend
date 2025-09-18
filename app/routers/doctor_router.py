# app/routers/doctors.py
from fastapi import APIRouter, Depends, HTTPException,Path
from sqlalchemy.orm import Session # type: ignore
from app.schemas.doctor import DoctorBase,DoctorCreate,DoctorResponse
from app.services import doctor_service
from app.core.database import get_db

router = APIRouter(tags=["Doctors"])

@router.post("/doctor")
def create_doctor(doctor:DoctorCreate, db: Session = Depends(get_db)):
    return doctor_service.create_doctor(db,doctor)

@router.get("/doctor", response_model=list[DoctorResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    return doctor_service.get(db)

@router.get("/doctor/{doctor_id}",response_model=DoctorResponse)
def view_doctor(
    doctor_id: int = Path(..., description="ID of the doctor", example="1"),
    db: Session = Depends(get_db)
):
    """
    Endpoint: GET /doctor/{doctor_id}
    Recieves a single doctor ID and passes the query to the service layer.

    Args:
        doctor_id (int): Unique ID of the doctor.
        db (Session): Database session.
    """
    return doctor_service.view_doctor(db, doctor_id)

@router.delete("/delete/{doctor_id}")
def delete(doctor_id: int, db: Session = Depends(get_db)):
    """
    Endpoint: DELETE /delete/{doctor_id}
    Receives follwoing arguments and pass them to doctor_delete() method in service layer.

    Args:
        doctor_id (int): ID of the doctor to delete.
        db (Session): Database session.
    """
    return doctor_service.doctor_delete(db, doctor_id)
