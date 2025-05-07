from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import SessionLocal
from ..utils.security import get_current_user

router = APIRouter(
    prefix="/usage",
    tags=["usage"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/me", response_model=List[schemas.UsageRecord], status_code=status.HTTP_200_OK
)
def get_my_usage(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Query all UsageRecord rows for the authenticated user
    return (
        db.query(models.UsageRecord)
        .filter(models.UsageRecord.user_id == current_user.id)
        .all()
    )
