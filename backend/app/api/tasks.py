from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Notification, Task, User, UserRole
from app.schemas.task import TaskAssignRequest, TaskCreate, TaskOut, TaskStatusUpdate
from app.services.assignment import auto_assign_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/project/{project_id}", response_model=TaskOut)
def create_task(project_id: int, payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = Task(project_id=project_id, **payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)

    auto_assign_task(db, task)
    return task


@router.patch("/{task_id}/assign", response_model=TaskOut)
def assign_task(task_id: int, payload: TaskAssignRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if payload.assignee_id is None:
        return auto_assign_task(db, task)

    assignee = db.query(User).filter(User.id == payload.assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignee not found")
    if assignee.role != task.required_role and assignee.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee role mismatch")

    task.assignee_id = assignee.id
    db.add(Notification(user_id=assignee.id, message=f"Manual assignment: '{task.title}'"))
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}/status", response_model=TaskOut)
def update_task_status(task_id: int, payload: TaskStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if current_user.role != UserRole.ADMIN and task.assignee_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot update this task")

    task.status = payload.status
    db.commit()
    db.refresh(task)
    return task


@router.get("/me", response_model=list[TaskOut])
def my_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.assignee_id == current_user.id).all()
