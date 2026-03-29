# AI-Powered Task Allocation System (MVP)

A full-stack project management application that analyzes textual requirements, suggests task breakdowns, and assigns tasks to developers/designers based on role and skills.

## 1) Folder Structure

```text
Task-Allocation-System-for-Software-Teams/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── seed/
│   │   └── services/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   └── types/
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## 2) Backend Code

### Architecture
- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Auth:** JWT (python-jose) + bcrypt password hashing
- **AI Task Breakdown:** Rules-based AI planner service (`services/ai_planner.py`), replaceable with real LLM service.
- **Auto Assignment:** Role + skills matching (`services/assignment.py`).

### Main backend modules
- `app/main.py` – app bootstrap, CORS, router registration.
- `app/models/models.py` – SQLAlchemy models and enums.
- `app/api/*.py` – domain routes (auth, projects, tasks, notifications, admin).
- `app/core/security.py` – password hashing and token generation/verification.
- `app/seed/seed_data.py` – test/demo seed data.

## 3) Frontend Code

### Architecture
- **Framework:** React + TypeScript + Vite
- **Styling:** Tailwind CSS
- **State:** Local component state + auth context
- **API Client:** Axios with auth token interceptor

### Main frontend modules
- `src/pages/LoginPage.tsx` – JWT login flow
- `src/pages/DashboardPage.tsx` – project creation, AI breakdown trigger, Kanban and notifications
- `src/components/KanbanBoard.tsx` – task status columns (To Do / In Progress / Done)
- `src/components/ProjectForm.tsx` – requirement text input + project creation
- `src/context/AuthContext.tsx` – token persistence and auth context

## 4) Database Schema

### Entity Relationships
- **Users (1) -> (N) Tasks** through `tasks.assignee_id`
- **Users (1) -> (N) Notifications**
- **Projects (1) -> (N) Tasks**
- **Users (1) -> (N) Projects** through `projects.created_by_id`

### Tables

#### users
- `id` (PK)
- `full_name`
- `email` (unique)
- `hashed_password`
- `role` (ADMIN | FRONTEND | BACKEND | DESIGNER)
- `skills` (comma-separated)
- `created_at`

#### projects
- `id` (PK)
- `name`
- `description`
- `requirements_text`
- `created_by_id` (FK -> users.id)
- `created_at`

#### tasks
- `id` (PK)
- `title`
- `description`
- `required_role`
- `status` (TODO | IN_PROGRESS | DONE)
- `priority`
- `project_id` (FK -> projects.id)
- `assignee_id` (FK -> users.id, nullable)
- `created_at`

#### notifications
- `id` (PK)
- `user_id` (FK -> users.id)
- `message`
- `is_read`
- `created_at`

## 5) API Endpoints

Base URL: `/api/v1`

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Projects
- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}/tasks`
- `POST /projects/{project_id}/ai-breakdown`

### Tasks
- `POST /tasks/project/{project_id}`
- `PATCH /tasks/{task_id}/assign`
- `PATCH /tasks/{task_id}/status`
- `GET /tasks/me`

### Notifications
- `GET /notifications/me`
- `PATCH /notifications/{notification_id}/read`

### Admin
- `GET /admin/users`
- `GET /admin/tasks`

## 6) Setup Guide

## Prerequisites
- Python 3.11+
- Node.js 20+

### Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Seed sample data
```bash
cd backend
python -m app.seed.seed_data
```

Seed credentials:
- `admin@example.com` / `password123`
- `frontend@example.com` / `password123`
- `backend@example.com` / `password123`
- `designer@example.com` / `password123`

### Frontend setup
```bash
cd frontend
npm install
npm run dev
```

Optional env for frontend:
```bash
# frontend/.env
VITE_API_URL=http://localhost:8000/api/v1
```

## Production-readiness notes
- Move secrets to environment manager (Vault, AWS Secrets Manager, etc.)
- Add DB migrations via Alembic before production
- Replace rules-based AI planner with LLM pipeline
- Add WebSocket notifications for real-time events
- Add centralized logging, rate limiting, and test coverage
