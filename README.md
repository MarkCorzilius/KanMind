# 📦 KanMind Backend API

## 📌 Description
KanMind is a Kanban board backend built with Django and Django REST Framework.  
It includes user authentication, boards, tasks, comments, and task visualization features such as assigned tasks and task counts.

---

## ⚙️ Tech Stack
- Django
- Django REST Framework
- SQLite

---

## 🚀 Quickstart Instructions

- Clone the repository
```bash
git clone <your-repo-url>
```

- Create a virtual environment:
```bash
python -m venv venv
```

- Activate Virtual Environment:
Windows:
```bash
venv\Scripts\activate
```
Mac:
```bash
source venv/bin/activate
```

- Install Dependencies:
```bash
pip install -r requirements.txt
```

- Run Database Migrations:
```bash
python manage.py migrate
```

- Create Superuser:
```bash
python manage.py createsuperuser
```

- Run Server:
```bash
python manage.py runserver
```

---

# 📡 API Overview

## 🔐 Authentication
- POST /api/registration/ → register user
- POST /api/login/ → login user + get token

---

## 📊 Boards
- GET /api/boards/ → list boards
- POST /api/boards/ → create board
- GET /api/boards/{board_id}/ → get board details
- PATCH /api/boards/{board_id}/ → update board
- DELETE /api/boards/{board_id}/ → delete board
- GET /api/email-check/ → check if email exists

---

## ✅ Tasks
- GET /api/tasks/assigned-to-me/ → tasks assigned to me
- GET /api/tasks/reviewing/ → tasks in review
- POST /api/tasks/ → create task
- PATCH /api/tasks/{task_id}/ → update task
- DELETE /api/tasks/{task_id}/ → delete task

---

## 💬 Comments
- GET /api/tasks/{task_id}/comments/ → list comments
- POST /api/tasks/{task_id}/comments/ → add comment
- DELETE /api/tasks/{task_id}/comments/{comment_id}/ → delete comment

---

# 🧪 Testing

- Use Postman to test API
- Register or login first
- Copy token from login response

```bash
Authorization: Token <your_token>
```
