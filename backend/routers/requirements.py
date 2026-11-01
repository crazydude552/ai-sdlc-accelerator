from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Requirement
from backend.schemas import RequirementCreate, RequirementResponse

print("Requirements router loaded")

router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"]
)

@router.post("/", response_model=RequirementResponse)
def create_requirement(
        requirement: RequirementCreate,
        db: Session = Depends(get_db)
):
    db_requirement = Requirement(
        project_id=requirement.project_id,
        title=requirement.title,
        description=requirement.description,
        type=requirement.type,
        priority=requirement.priority,
        status=requirement.status
    )

    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)

    return db_requirement

@router.get("/", response_model=List[RequirementResponse])
def get_requirements(
        db: Session = Depends(get_db)
):
    return db.query(Requirement).all()

@router.get("/{requirement_id}", response_model=RequirementResponse)
def get_requirement(
        requirement_id: int,
        db: Session = Depends(get_db)
):
    requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id
    ).first()

    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")

    return requirement

@router.put("/{requirement_id}", response_model=RequirementResponse)
def update_requirement(
        requirement_id: int,
        requirement_data: RequirementCreate,
        db: Session = Depends(get_db)
):
    requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id
    ).first()

    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")

    requirement.project_id = requirement_data.project_id
    requirement.title = requirement_data.title
    requirement.description = requirement_data.description
    requirement.type = requirement_data.type
    requirement.priority = requirement_data.priority
    requirement.status = requirement_data.status

    db.commit()
    db.refresh(requirement)

    return requirement

@router.delete("/{requirement_id}")
def delete_requirement(
        requirement_id: int,
        db: Session = Depends(get_db)
):
    requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id
    ).first()

    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")

    db.delete(requirement)
    db.commit()

    return {"message": "Requirement deleted successfully"}