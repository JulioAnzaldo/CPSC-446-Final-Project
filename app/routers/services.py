from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import SessionLocal
from ..utils.access import require_read_access
from ..utils.security import get_current_user

router = APIRouter(prefix="/services", tags=["services"])


# Return db connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/", response_model=schemas.CloudService, status_code=status.HTTP_201_CREATED
)
def create_service(
    svc_in: schemas.CloudServiceCreate,
    db: Session = Depends(get_db),
):
    # Prevent duplicates
    if db.query(models.CloudService).filter_by(name=svc_in.name).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Service with that name already exists",
        )
    svc = models.CloudService(
        name=svc_in.name,
        description=svc_in.description,
    )
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return svc


@router.get(
    "/", response_model=List[schemas.CloudService], status_code=status.HTTP_200_OK
)
def list_services(db: Session = Depends(get_db)):
    return db.query(models.CloudService).all()


@router.get(
    "/{service_id}",
    response_model=schemas.CloudService,
    status_code=status.HTTP_200_OK,
)
def get_service(service_id: int, db: Session = Depends(get_db)):
    svc = db.query(models.CloudService).get(service_id)
    if not svc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    return svc


@router.put(
    "/{service_id}", response_model=schemas.CloudService, status_code=status.HTTP_200_OK
)
def update_service(
    service_id: int,
    svc_in: schemas.CloudServiceCreate,
    db: Session = Depends(get_db),
):
    svc = db.query(models.CloudService).get(service_id)
    if not svc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    svc.name = svc_in.name
    svc.description = svc_in.description
    db.commit()
    db.refresh(svc)
    return svc


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    svc = db.query(models.CloudService).get(service_id)
    if not svc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    db.delete(svc)
    db.commit()
    return


@router.get(
    "/{service_id}/call",
    response_model=schemas.CloudService,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_read_access)],
)
def call_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Dummy endpoint that simulates calling the cloud service.
    Only users with the "read" permission may access it.
    Also logs usage on each successful call.
    """
    svc = db.query(models.CloudService).get(service_id)
    if not svc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )

    # --- Usage tracking ---
    record = models.UsageRecord(
        user_id=current_user.id,
        service_id=service_id,
    )
    db.add(record)
    db.commit()
    # ------------------------

    return svc
