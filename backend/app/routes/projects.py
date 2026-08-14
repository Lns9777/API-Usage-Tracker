from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Project
from ..schemas import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    existing = db.query(Project).filter(Project.name == project.name).first()
    if existing:
        return existing
    row = Project(**project.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    row = db.query(Project).filter(Project.id == project_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    return row


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    row = db.query(Project).filter(Project.id == project_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    row = db.query(Project).filter(Project.id == project_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(row)
    db.commit()
    return {"success": True}
