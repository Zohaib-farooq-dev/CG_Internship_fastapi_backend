from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.patient_models import Patient as PatientDB   # SQLAlchemy model
from app.schemas.patients import Patient, PatientUpdate

def view(db: Session):
    return db.query(PatientDB).all()

def view_patient(db: Session, patient_id: str):
    patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found!")
    return patient

def sorted_patients(db: Session, sort_by: str, order: str):
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

def create_patient(db: Session, patient: Patient):
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

def update_patient(db: Session, patient_id: str, patient: PatientUpdate):
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

def patient_delete(db: Session, patient_id: str):
    db_patient = db.query(PatientDB).filter(PatientDB.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found!")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted"}
