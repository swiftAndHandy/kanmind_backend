# KanMind Backend

A RESTful API backend for the KanMind project management application, built with Django and Django REST Framework.

---

## Requirements

- Python 3.10+
- pip

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/swiftAndHandy/kanmind_backend.git
cd kanmind_backend
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## Admin Panel

The Django admin panel is available at `http://127.0.0.1:8000/admin/`.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Login and receive an auth token |
| GET | `/api/email-check/` | Check if an email address is registered |

### Boards

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/boards/` | List all boards the user is a member or owner of |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/{board_id}/` | Retrieve board details including tasks |
| PATCH | `/api/boards/{board_id}/` | Update board title or members |
| DELETE | `/api/boards/{board_id}/` | Delete a board (owner only) |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/assigned-to-me/` | List tasks assigned to the current user |
| GET | `/api/tasks/reviewing/` | List tasks where the current user is reviewer |
| POST | `/api/tasks/` | Create a new task |
| PATCH | `/api/tasks/{task_id}/` | Update a task |
| DELETE | `/api/tasks/{task_id}/` | Delete a task (creator or board owner only) |

### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/{task_id}/comments/` | List all comments for a task |
| POST | `/api/tasks/{task_id}/comments/` | Add a comment to a task |
| DELETE | `/api/tasks/{task_id}/comments/{comment_id}/` | Delete a comment (author only) |

---

## Authentication

This API uses **Token Authentication**. After login or registration, include the token in the `Authorization` header of all subsequent requests:

```
Authorization: Token <your_token_here>
```

---

## Project Structure

```
kanmind/
├── core/               # Project settings and main URL configuration
├── auth_app/           # User authentication and registration
├── board_app/          # Board management
├── task_app/           # Task and comment management
└── manage.py
```