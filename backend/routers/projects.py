from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Project
from backend.schemas import ProjectCreate, ProjectResponse  # <-- Added ProjectResponse

print("Projects router loaded")
router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post("/", response_model=ProjectResponse)
def create_project(
        project: ProjectCreate,
        db: Session = Depends(get_db)
):
    db_project = Project(
        project_name=project.project_name,
        description=project.description,
        division=project.division,
        status=project.status,
        version=project.version
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

@router.get("/", response_model=List[ProjectResponse])  # <-- Added response_model
def get_projects(
        db: Session = Depends(get_db)
):
    return db.query(Project).all()

@router.get("/{project_id}", response_model=ProjectResponse)  # <-- Added response_model
def get_project(
        project_id: int,
        db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project

@router.put("/{project_id}", response_model=ProjectResponse)  # <-- Added response_model
def update_project(
        project_id: int,
        project_data: ProjectCreate,
        db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    project.project_name = project_data.project_name
    project.description = project_data.description
    project.division = project_data.division
    project.status = project_data.status
    project.version = project_data.version

    db.commit()
    db.refresh(project)

    return project

@router.delete("/{project_id}")
def delete_project(
        project_id: int,
        db: Session = Depends(get_db)
):

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }