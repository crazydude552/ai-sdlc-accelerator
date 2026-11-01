from pydantic import BaseModel
from typing import List


# --- Requirement Schemas (Placed first so ProjectResponse can reference it) ---
class RequirementCreate(BaseModel):
    project_id: int
    title: str
    description: str
    type: str       # e.g., Functional, Non-Functional
    priority: str   # e.g., Major, Critical, Minor
    status: str     # e.g., New, Draft, Approved


class RequirementResponse(RequirementCreate):
    id: int

    class Config:
        from_attributes = True


# --- Project Schemas ---
class ProjectCreate(BaseModel):
    project_name: str
    description: str
    division: str
    status: str
    version: str


class ProjectResponse(ProjectCreate):
    id: int
    requirements: List[RequirementResponse] = []  # Nests all requirements for this project

    class Config:
        from_attributes = True