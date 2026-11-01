from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String)
    description = Column(String)
    division = Column(String)
    status = Column(String)
    version = Column(String)

    # Relationship to easily fetch requirements for a project
    requirements = relationship("Requirement", back_populates="project", cascade="all, delete-orphan")


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    title = Column(String)
    description = Column(String)
    type = Column(String)  # e.g., Functional, Non-Functional
    priority = Column(String)  # e.g., Major, Critical, Minor
    status = Column(String)  # e.g., New, Draft, Approved

    # Relationship back to the project
    project = relationship("Project", back_populates="requirements")