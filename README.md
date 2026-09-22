# 📦 KanMind (Kanban Board Backend API)

## 📌 Description

KanMind is a RESTful backend API for a Kanban board application, built with Python, Django, and Django REST Framework.
It provides user authentication, board and task management, comments, task assignments, and task review workflows.

## Features

- User registration and authentication
- Token-based API authorization
- Board creation and management
- Task creation, updates, and deletion
- Tasks assigned to the current user
- Tasks currently under review
- Comment creation and deletion
- Email availability checks
- Database management with PostgreSQL
- Automated API testing

## ⚙️ Tech Stack

- Python 3.14.0
- Django 6.0.6
- Django REST Framework 3.17.1
- PostgreSQL
- AWS EC2 for deployment
- AWS RDS for managed PostgreSQL
- AWS ECR for Docker image storage

---

## 🚀 Quickstart Instructions

Clone the repository.

```bash
git clone <your-repo-url>
```

Copy the environment template and fill in your own values.

```bash
cp .env.template .env
```

Build and start all services with Docker Compose.

```bash
docker compose -f compose.dev.yaml up --build -d
```

Follow the backend container logs.

```bash
docker compose -f compose.dev.yaml logs -f web
```

Stop all running containers.

```bash
docker compose -f compose.dev.yaml down
```

The development API is exposed through the `web` service configured in `compose.dev.yaml`.

---

# 📡 API Overview

## 🔐 Authentication

- POST `/api/registration/` → register a user
- POST `/api/login/` → log in and receive an authentication token
- GET `/api/email-check/` → check whether an email address exists

---

## 📊 Boards

- GET `/api/boards/` → list boards
- POST `/api/boards/` → create a board
- GET `/api/boards/{board_id}/` → get board details
- PATCH `/api/boards/{board_id}/` → update a board
- DELETE `/api/boards/{board_id}/` → delete a board

---

## ✅ Tasks

- POST `/api/tasks/` → create a task
- GET `/api/tasks/{task_id}/` → get task details
- PATCH `/api/tasks/{task_id}/` → update a task
- DELETE `/api/tasks/{task_id}/` → delete a task
- GET `/api/tasks/assigned-to-me/` → list tasks assigned to the current user
- GET `/api/tasks/reviewing/` → list tasks currently under review

---

## 💬 Comments

- GET `/api/tasks/{task_id}/comments/` → list comments for a task
- POST `/api/tasks/{task_id}/comments/` → add a comment to a task
- DELETE `/api/tasks/{task_id}/comments/{comment_id}/` → delete a comment

---

# 🧪 Testing

Run the complete Django test suite inside the running backend container:

```bash
docker compose -f compose.dev.yaml exec web python manage.py test
```

Run tests for a single app:

```bash
docker compose -f compose.dev.yaml exec web python manage.py test accounts_app
```

You can also use Postman or another API client to test the endpoints.

Register or log in first, then copy the token from the login response and send it with protected requests:

```http
Authorization: Token <your_token>
```
