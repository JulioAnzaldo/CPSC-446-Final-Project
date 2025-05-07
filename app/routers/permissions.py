from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import SessionLocal

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/", response_model=schemas.Permission, status_code=status.HTTP_201_CREATED
)
def create_permission(
    p_in: schemas.PermissionCreate,
    db: Session = Depends(get_db),
):
    # Check whether a permission with the same name and service already exists
    existing = (
        db.query(models.Permission)
        .filter(
            models.Permission.name == p_in.name,
            models.Permission.service_name == p_in.service_name,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission already exists",
        )
    # Create and persist a new Permission record
    perm = models.Permission(
        name=p_in.name,
        service_name=p_in.service_name,
    )
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


@router.get(
    "/", response_model=List[schemas.Permission], status_code=status.HTTP_200_OK
)
def list_permissions(db: Session = Depends(get_db)):
    # Retrieve all Permission records
    return db.query(models.Permission).all()
