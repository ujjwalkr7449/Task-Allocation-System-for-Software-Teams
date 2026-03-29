from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Project, Task, User
from app.schemas.project import ProjectCreate, ProjectOut
from app.schemas.task import TaskOut
from app.services.ai_planner import suggest_tasks_from_requirements
from app.services.assignment import auto_assign_task

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = Project(
        name=payload.name,
        description=payload.description,
        requirements_text=payload.requirements_text,
        created_by_id=current_user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Project).order_by(Project.created_at.desc()).all()


@router.get("/{project_id}/tasks", response_model=list[TaskOut])
def list_project_tasks(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db.query(Task).filter(Task.project_id == project_id).all()


@router.post("/{project_id}/ai-breakdown", response_model=list[TaskOut])
def generate_tasks(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    suggestions = suggest_tasks_from_requirements(project.requirements_text)
    created_tasks: list[Task] = []
    for item in suggestions:
        task = Task(project_id=project.id, **item)
        db.add(task)
        db.flush()
        created_tasks.append(task)

    db.commit()

    for task in created_tasks:
        auto_assign_task(db, task)

    return created_tasks
