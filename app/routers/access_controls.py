from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import SessionLocal

router = APIRouter(prefix="/access-controls", tags=["access-controls"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/", response_model=schemas.AccessControl, status_code=status.HTTP_201_CREATED
)
def assign_permission(
    ac_in: schemas.AccessControlCreate,
    db: Session = Depends(get_db),
):
    # Verify user exists
    user = db.query(models.User).get(ac_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify service exists
    service = db.query(models.CloudService).get(ac_in.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Prevent duplicate assignment
    exists = (
        db.query(models.AccessControl)
        .filter_by(
            user_id=ac_in.user_id,
            service_id=ac_in.service_id,
            permission=ac_in.permission,
        )
        .first()
    )
    if exists:
        raise HTTPException(
            status_code=409,
            detail="This permission is already assigned to the user for this service",
        )

    ac = models.AccessControl(
        user_id=ac_in.user_id,
        service_id=ac_in.service_id,
        permission=ac_in.permission,
    )
    db.add(ac)
    db.commit()
    db.refresh(ac)
    return ac


@router.get(
    "/", response_model=List[schemas.AccessControl], status_code=status.HTTP_200_OK
)
def list_access_controls(db: Session = Depends(get_db)):
    return db.query(models.AccessControl).all()


@router.get(
    "/{ac_id}", response_model=schemas.AccessControl, status_code=status.HTTP_200_OK
)
def get_access_control(ac_id: int, db: Session = Depends(get_db)):
    ac = db.query(models.AccessControl).get(ac_id)
    if not ac:
        raise HTTPException(status_code=404, detail="Access control not found")
    return ac


# Remove access
@router.delete("/{ac_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_access(ac_id: int, db: Session = Depends(get_db)):
    ac = db.query(models.AccessControl).get(ac_id)
    if not ac:
        raise HTTPException(status_code=404, detail="Access control not found")
    db.delete(ac)
    db.commit()
    return
