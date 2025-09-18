from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.patient_models import Patient as PatientDB   # SQLAlchemy model
from app.schemas.patients import Patient, PatientUpdate

def view(db: Session)->list[PatientDB]:
    """Return a list of all patients from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        PatientDB: Patients record if found.
    """
    return db.query(PatientDB).all()

def view_patient(db: Session, patient_id: str)->PatientDB:
    
    """
    Retrieve a single patient's details by their unique ID.

    Args:
        patient_id (str): Patient ID to look up (e.g., "P001").
        db (Session): SQLAlchemy database session.

    Returns:
        PatientDB: Patient record if found.

    Raises:
        HTTPException: 404 if patient is not found.
    """
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found!")
    return patient

def sorted_patients(db: Session, sort_by: str, order: str)->list[PatientDB]:
    """
    Retrieve patients sorted by a specified field and order.

    Args:
        sort_by (str): Column to sort on ('weight', 'height', or 'bmi'). Defaults to 'weight'.
        order (str): Sort order ('asc' or 'desc'). Defaults to 'asc'.
        db (Session): SQLAlchemy database session.

    Returns:
        list[PatientDB]: Sorted list of patients.

    Raises:
        HTTPException: 400 if invalid field or order is provided.
    """
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Use one of {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use asc or desc")

    query = db.query(PatientDB)
    column = getattr(PatientDB, sort_by)
    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())
    return query.all()

def create_patient(db: Session, patient: Patient)->dict:
    """
    Create a new patient record.

    Args:
        patient (Patient): Request body validated using Pydantic with
                           all required patient details.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Success message if creation is successful.

    Raises:
        HTTPException: 400 if a patient with the same ID already exists.
    """
    # Check if patient already exists
    existing = db.query(PatientDB).filter(PatientDB.id == patient.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient already exists!")

    db_patient = PatientDB(
        id=patient.id,
        name=patient.name,
        city=patient.city,
        age=patient.age,
        gender=patient.gender,
        height=patient.height,
        weight=patient.weight,
        bmi=patient.bmi,            # computed_field se direct
        verdict=patient.verdict     # computed_field se direct
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return {"message": "Patient created successfully"}

def update_patient(db: Session, patient_id: str, patient: PatientUpdate)->dict:
    """
    Update an existing patient's details.

    Args:
        patient_id (str): ID of the patient to update.
        patient (PatientUpdate): Pydantic model containing fields to update
                                 (only provided fields will be modified).
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Success message upon successful update.

    Raises:
        HTTPException: 404 if patient is not found.
    """
    db_patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found!")

    for field, value in patient.model_dump(exclude_unset=True).items():
        setattr(db_patient, field, value)

    # Recompute BMI/Verdit if weight or height changed
    if patient.height or patient.weight:
        h = patient.height or db_patient.height
        w = patient.weight or db_patient.weight
        db_patient.bmi = round(w / (h ** 2), 2)
        db_patient.verdict = (
            "Underweight" if db_patient.bmi < 18.5
            else "Normal" if db_patient.bmi < 28
            else "Obese"
        )

    db.commit()
    db.refresh(db_patient)
    return {"message": "Patient updated successfully"}

def patient_delete(db: Session, patient_id: str)->JSONResponse:
    """
    Delete a patient record by ID.

    Args:
        patient_id (str): ID of the patient to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        JSONResponse: 204 No Content on successful deletion.

    Raises:
        HTTPException: 404 if patient is not found.
    """
    db_patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found!")
    db.delete(db_patient)
    db.commit()
    return JSONResponse(status_code=204)
