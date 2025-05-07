from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..db import SessionLocal
from .security import get_current_user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_access(
    service_id: int,
    permission: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Ensure the service exists
    svc = db.query(models.CloudService).get(service_id)
    if not svc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")

    # Check permission
    has_perm = (
        db.query(models.AccessControl)
        .filter_by(
            user_id=current_user.id,
            service_id=service_id,
            permission=permission,
        )
        .first()
    )
    if not has_perm:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"User '{current_user.username}' lacks '{permission}' on '{svc.name}'",
        )

    # Enforce per-minute rate limit
    limit = svc.max_calls_per_minute
    cutoff = datetime.utcnow() - timedelta(minutes=1)
    recent_count = (
        db.query(models.UsageRecord)
        .filter(
            models.UsageRecord.user_id == current_user.id,
            models.UsageRecord.service_id == service_id,
            models.UsageRecord.timestamp >= cutoff,
        )
        .count()
    )
    if recent_count >= limit:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"Rate limit exceeded: {recent_count} calls in the last minute "
                f"(limit {limit})"
            ),
        )

    return True


# Helper function
def require_read_access(
    service_id: int,
    _ok: bool = Depends(
        lambda service_id, current_user=Depends(get_current_user), db=Depends(
            get_db
        ): verify_access(service_id, "read", current_user, db)
    ),
):
    """
    Dummy dependency that binds service_id to verify_access(..., "read")
    so FastAPI can see the parameter and include the endpoint in OpenAPI.
    """
    return True
