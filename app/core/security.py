from passlib.context import CryptContext # type: ignore
from jose import jwt, JWTError # type: ignore
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "supersecret"    # env se lena better
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    """
    Hash a plain-text password using bcrypt.

    Args:
        password (str): User's plain password.

    Returns:
        str: Secure bcrypt hash of the password.
    """
    print("Password received:", repr(password))

    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    """
    Verify that a plain password matches a stored hash.

    Args:
        plain (str): Plain password provided by the user.
        hashed (str): Previously stored bcrypt hash.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    """
    Create a signed JWT access token.

    Adds an expiration claim (`exp`) to the provided data and encodes
    it using the configured secret key and algorithm.

    Args:
        data (dict): Payload data to include inside the token.  
                     Typically includes a user/doctor ID under the `"sub"` key.

    Returns:
        str: Encoded JWT token string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_doctor_id(token: str = Depends(oauth2_scheme)):
    """
    Extract the current doctor's ID from a validated JWT.

    This function is used as a FastAPI dependency to protect routes.
    It decodes the incoming Bearer token, retrieves the `"sub"` claim,
    and returns it as an integer.

    Args:
        token (str): Automatically provided OAuth2 Bearer token.

    Raises:
        HTTPException: If the token is missing, invalid, expired,
                       or does not contain a `"sub"` field.

    Returns:
        int: Doctor's unique ID contained in the token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        doctor_id = payload.get("sub")
        if doctor_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return int(doctor_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
