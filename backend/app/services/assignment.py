from sqlalchemy.orm import Session

from app.models.models import Notification, Task, User


def auto_assign_task(db: Session, task: Task) -> Task:
    """Assign task to a developer with matching role and highest skills overlap."""
    candidates = db.query(User).filter(User.role == task.required_role).all()
    if not candidates:
        return task

    def score(user: User) -> int:
        text = f"{task.title} {task.description}".lower()
        skills = [s.strip().lower() for s in user.skills.split(",") if s.strip()]
        return sum(1 for skill in skills if skill in text)

    assignee = sorted(candidates, key=score, reverse=True)[0]
    task.assignee_id = assignee.id

    db.add(
        Notification(
            user_id=assignee.id,
            message=f"You have been assigned '{task.title}' for project #{task.project_id}.",
        )
    )
    db.commit()
    db.refresh(task)
    return task
