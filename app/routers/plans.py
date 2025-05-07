from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import SessionLocal

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Plan, status_code=status.HTTP_201_CREATED)
def create_plan(
    p_in: schemas.PlanCreate,
    db: Session = Depends(get_db),
):
    # Prevent creation of duplicate plan names
    if db.query(models.Plan).filter_by(name=p_in.name).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Plan name already exists",
        )
    # Fetch Permission objects by provided IDs
    permissions = (
        db.query(models.Permission)
        .filter(models.Permission.id.in_(p_in.permission_ids))
        .all()
    )
    # Create and persist a new Plan with associated permissions
    plan = models.Plan(
        name=p_in.name,
        description=p_in.description,
        max_calls_per_minute=p_in.max_calls_per_minute,
        permissions=permissions,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/", response_model=List[schemas.Plan], status_code=status.HTTP_200_OK)
def list_plans(db: Session = Depends(get_db)):
    # Retrieve all Plan records
    return db.query(models.Plan).all()


@router.put("/{plan_id}", response_model=schemas.Plan, status_code=status.HTTP_200_OK)
def update_plan(
    plan_id: int,
    p_in: schemas.PlanCreate,
    db: Session = Depends(get_db),
):
    # Locate existing Plan by ID
    plan = db.get(models.Plan, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )
    # Update fields and associated permissions
    plan.name = p_in.name
    plan.description = p_in.description
    plan.max_calls_per_minute = p_in.max_calls_per_minute
    plan.permissions = (
        db.query(models.Permission)
        .filter(models.Permission.id.in_(p_in.permission_ids))
        .all()
    )
    db.commit()
    db.refresh(plan)
    return plan


@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    # Remove a Plan by ID
    plan = db.get(models.Plan, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )
    db.delete(plan)
    db.commit()
    return
