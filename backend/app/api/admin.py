from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.models import Task, User
from app.schemas.task import TaskOut
from app.schemas.user import UserOut

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(User).all()


@router.get("/tasks", response_model=list[TaskOut])
def list_all_tasks(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(Task).all()
