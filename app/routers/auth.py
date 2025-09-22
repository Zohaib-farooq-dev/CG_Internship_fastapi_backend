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
    """
    Register a new doctor account.

    Checks if the provided email is already registered.  
    If unique, creates a new `Doctor` record in the database.

    Args:
        doctor (DoctorCreate): Pydantic schema containing
            name, email, and password for the new doctor.
        db (Session): SQLAlchemy database session (provided by dependency).

    Raises:
        HTTPException (400): If the email is already in use.

    Returns:
        dict: Confirmation message after successful creation.
              Example: {"msg": "Doctor created"}
    """
    if db.query(Doctor).filter(Doctor.email == doctor.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    doctor = create_doctor(db, doctor) 
    return {"msg": "Doctor created"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a doctor and return a JWT access token.

    Uses OAuth2 password flow.  
    Validates the provided email (received as `username`) and password.
    On success, generates a signed JWT containing the doctor's ID
    in the `"sub"` (subject) claim.

    Args:
        form_data (OAuth2PasswordRequestForm): Parsed login form with
            `username` (doctor email) and `password`.
        db (Session): SQLAlchemy database session.

    Raises:
        HTTPException (401): If email does not exist or password is invalid.

    Returns:
        dict: Access token and token type for Bearer authentication.
              Example:
              {
                  "access_token": "<jwt_token>",
                  "token_type": "bearer"
              }
    """
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
