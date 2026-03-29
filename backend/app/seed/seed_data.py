"""Seed script with demo users, project, and tasks."""

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.models import Project, Task, User, UserRole


def run_seed() -> None:
    db = SessionLocal()

    if db.query(User).count() > 0:
        print("Database already seeded.")
        return

    users = [
        User(
            full_name="Alice Admin",
            email="admin@example.com",
            hashed_password=get_password_hash("password123"),
            role=UserRole.ADMIN,
            skills="management,planning",
        ),
        User(
            full_name="Fiona Frontend",
            email="frontend@example.com",
            hashed_password=get_password_hash("password123"),
            role=UserRole.FRONTEND,
            skills="react,tailwind,typescript",
        ),
        User(
            full_name="Ben Backend",
            email="backend@example.com",
            hashed_password=get_password_hash("password123"),
            role=UserRole.BACKEND,
            skills="fastapi,sqlalchemy,jwt",
        ),
        User(
            full_name="Diana Designer",
            email="designer@example.com",
            hashed_password=get_password_hash("password123"),
            role=UserRole.DESIGNER,
            skills="figma,ux,wireframe",
        ),
    ]
    db.add_all(users)
    db.commit()

    admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
    project = Project(
        name="AI Task Allocation MVP",
        description="Build and deploy MVP dashboard",
        requirements_text="""
        Design clean project dashboard UI
        Build REST API for auth and project management
        Implement Kanban board interactions in React
        Create database models and migration scripts
        """,
        created_by_id=admin_user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    db.add_all(
        [
            Task(
                title="Design dashboard wireframe",
                description="Create primary dashboard flow and component map",
                required_role=UserRole.DESIGNER,
                project_id=project.id,
            ),
            Task(
                title="Implement authentication API",
                description="JWT-based auth with login/register",
                required_role=UserRole.BACKEND,
                project_id=project.id,
            ),
            Task(
                title="Build Kanban board UI",
                description="Three columns with drag/drop placeholder",
                required_role=UserRole.FRONTEND,
                project_id=project.id,
            ),
        ]
    )
    db.commit()
    print("Seed completed.")


if __name__ == "__main__":
    run_seed()
