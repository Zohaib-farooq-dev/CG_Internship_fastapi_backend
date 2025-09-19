from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session # type: ignore
from app.core.database import get_db
from app.models.doctor_models import Doctor
from app.core.security import verify_password, create_access_token
from app.services.doctor_service import create_doctor
from app.schemas.doctor import DoctorCreate,DoctorLogin

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(doctor : DoctorCreate,db: Session = Depends(get_db) ):
    if db.query(Doctor).filter(Doctor.email == doctor.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    doctor = create_doctor(db, doctor) 
    return {"msg": "Doctor created"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username will contain the email
    doctor = db.query(Doctor).filter(Doctor.email == form_data.username).first()
    if not doctor or not verify_password(form_data.password, doctor.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(doctor.id)})
    return {"access_token": token, "token_type": "bearer"}
# @router.post("/login")
# def login(payload: DoctorLogin, db: Session = Depends(get_db)):
#     doctor = db.query(Doctor).filter(Doctor.email == payload.email).first()
#     if not doctor or not verify_password(payload.password, doctor.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token({"sub": str(doctor.id)})
#     return {"access_token": token, "token_type": "bearer"}

# @router.post("/login")
# def login(email: str, password: str, db: Session = Depends(get_db)):
#     doctor = db.query(Doctor).filter(Doctor.email == email).first()
#     if not doctor or not verify_password(password, doctor.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_access_token({"sub": str(doctor.id)})
#     return {"access_token": token, "token_type": "bearer"}
