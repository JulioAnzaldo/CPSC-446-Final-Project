from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.exc import UnknownHashError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..utils.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    get_db,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# Login
@router.post("/token", response_model=schemas.Token)
def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User).filter(models.User.username == form_data.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # safely verify—even if hashed_password is bad
    try:
        valid = verify_password(form_data.password, user.hashed_password)
    except UnknownHashError:
        valid = False

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        {"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
