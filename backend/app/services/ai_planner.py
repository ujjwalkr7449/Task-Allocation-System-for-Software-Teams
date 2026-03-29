from app.models.models import UserRole

ROLE_HINTS = {
    UserRole.FRONTEND: ["ui", "frontend", "react", "tailwind", "component"],
    UserRole.BACKEND: ["api", "backend", "database", "auth", "service"],
    UserRole.DESIGNER: ["design", "ux", "wireframe", "prototype", "figma"],
}


def suggest_tasks_from_requirements(requirements_text: str) -> list[dict]:
    """Simple rules-based planner to simulate AI suggestions in MVP."""
    tasks: list[dict] = []
    lines = [line.strip("-• ") for line in requirements_text.split("\n") if line.strip()]

    for idx, line in enumerate(lines, start=1):
        lowered = line.lower()
        role = UserRole.BACKEND
        for candidate_role, keywords in ROLE_HINTS.items():
            if any(keyword in lowered for keyword in keywords):
                role = candidate_role
                break

        tasks.append(
            {
                "title": f"Task {idx}: {line[:60]}",
                "description": line,
                "required_role": role,
                "priority": "MEDIUM",
            }
        )

    return tasks
