from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from sqlalchemy.orm import Session

from .. import models
from ..db import SessionLocal

# Secret key for signing JWTs
SECRET_KEY = "temp-key"
# Algorithm used for JWT encoding/decoding
ALGORITHM = "HS256"
# Token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Context for hashing passwords using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Bearer token scheme pointing to the token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    # Yield a new database session and ensure it is closed after use.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    # Hash a plaintext password using bcrypt.
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # Create a JWT with the provided data and expiration delta.
    to_encode = data.copy()
    # Calculate expiration time
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    # Encode and return the JWT
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    # Decode a JWT and return its payload, or empty dict on failure.
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return {}


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    # Retrieve the current user based on the JWT Bearer token.
    # Raises 401 if token is invalid or user does not exist.
    creds_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    username: str | None = payload.get("sub")
    # Ensure the token contains a username
    if username is None:
        raise creds_exc
    # Lookup user in database
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise creds_exc
    return user


def require_admin(current_user: models.User = Depends(get_current_user)) -> models.User:
    # Ensure the current user has the 'admin' role.
    # Raises 403 if not an admin.
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return current_user
