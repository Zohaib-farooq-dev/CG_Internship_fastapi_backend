from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session # type: ignore
from app.models.doctor_models import Doctor as doctordb  # SQLAlchemy model
from app.schemas.doctor import DoctorCreate
from app.core.security import hash_password

def get(db: Session):
    """Return a list of all doctors from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        PatientDB: Patients record if found.
    """
    return db.query(doctordb).all()

def view_doctor(db: Session, doctor_id: int):
    
    """
    Retrieve a single dcotor's details by their unique ID.

    Args:
        doctor_id (int): Doctor ID to look up (e.g., 1,2,3).
        db (Session): SQLAlchemy database session.

    Returns:
        doctordb: doctor record if found.

    Raises:
        HTTPException: 404 if patient is not found.
    """
    doctor = db.query(doctordb).filter(doctordb.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found!")
    return doctor

def create_doctor(db: Session, doctor: DoctorCreate)->dict:
    """
    Create a new doctor record.

    Args:
        doctor (DoctorCreate): Request body validated using Pydantic with
                           all required doctor details.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Success message if creation is successful.

    Raises:
        HTTPException: 400 if a doctor with the same ID already exists.
    """
    # Check if patient already exists
    existing = db.query(doctordb).filter(doctordb.email == doctor.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Doctor already exists!")
    
    hashed_pw = hash_password(doctor.password)

    db_doctor = doctordb(
         name = doctor.name,
         email = doctor.email,
         password = hashed_pw
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return {"message": "Patient created successfully"}

# def update_patient(db: Session, patient_id: str, patient: PatientUpdate)->dict:
#     """
#     Update an existing patient's details.

#     Args:
#         patient_id (str): ID of the patient to update.
#         patient (PatientUpdate): Pydantic model containing fields to update
#                                  (only provided fields will be modified).
#         db (Session): SQLAlchemy database session.

#     Returns:
#         dict: Success message upon successful update.

#     Raises:
#         HTTPException: 404 if patient is not found.
#     """
#     db_patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
#     if not db_patient:
#         raise HTTPException(status_code=404, detail="Patient not found!")

#     for field, value in patient.model_dump(exclude_unset=True).items():
#         setattr(db_patient, field, value)

#     # Recompute BMI/Verdit if weight or height changed
#     if patient.height or patient.weight:
#         h = patient.height or db_patient.height
#         w = patient.weight or db_patient.weight
#         db_patient.bmi = round(w / (h ** 2), 2)
#         db_patient.verdict = (
#             "Underweight" if db_patient.bmi < 18.5
#             else "Normal" if db_patient.bmi < 28
#             else "Obese"
#         )

#     db.commit()
#     db.refresh(db_patient)
#     return {"message": "Patient updated successfully"}

def doctor_delete(db: Session, doctor_id: int)->JSONResponse:
    """
    Delete a doctor record by ID.

    Args:
        dcotor_id (int): ID of the doctor to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        JSONResponse: 204 No Content on successful deletion.

    Raises:
        HTTPException: 404 if doctor is not found.
    """
    db_doctor = db.query(doctordb).filter(doctordb.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Patient not found!")
    db.delete(db_doctor)
    db.commit()
    return JSONResponse(status_code=204)
