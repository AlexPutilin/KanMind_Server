# Kanmind Backend

Kanmind Backend is a Django REST Framework API for a Kanban-style board and task management application.

It provides authentication, board management, task handling, task assignments, review workflows and comments.
The frontend is hosted separately and communicates with this backend through REST API endpoints.

---

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Docker
* Docker Compose
* Gunicorn
* Token Authentication

---

## Live-Demo

You can test the live demo here: [Kanmind Live Demo](https://kanmind.alexander-putilin.de/)

---

## Frontend

The frontend for this project is available in a separate repository:
https://github.com/AlexPutilin/KanMind_Frontend

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AlexPutilin/KanMind_Server.git .
```

2. Create a .env file in the project root:

```bash
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CSRF_TRUSTED_ORIGINS=http://your-domain.com,https://your-domain.com

DB_NAME=kanmind
DB_USER=kanmind_user
DB_PASSWORD=your-database-password
DB_HOST=db
DB_PORT=5432

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your-admin-password
```

3. Start the Docker containers:

```bash
docker compose up --build
```

The backend container automatically runs:
* `collectstatic`
* `makemigrations`
* `migrate`
* superuser creation from `.env`
* Gunicorn server

---

## Authentication

Token-based authentication is used.

After login or registration, include the token in requests:

```
Authorization: Token <your_token>
```

---

## API Endpoints

### Authentication

| Method | Endpoint             | Description               |
| ------ | -------------------- | ------------------------- |
| POST   | `/api/registration/` | Register a new user       |
| POST   | `/api/login/`        | Log in and retrieve token |
| GET    | `/api/email-check/`  | Check if an email exists  |

---

### Boards

| Method | Endpoint                  | Description                    |
| ------ | ------------------------- | ------------------------------ |
| GET    | `/api/boards/`            | List all boards                |
| POST   | `/api/boards/`            | Create a new board             |
| GET    | `/api/boards/{board_id}/` | Retrieve a board with tasks    |
| PATCH  | `/api/boards/{board_id}/` | Update board title and members |
| DELETE | `/api/boards/{board_id}/` | Delete a board                 |

---

### Tasks

| Method | Endpoint                     | Description                |
| ------ | ---------------------------- | -------------------------- |
| GET    | `/api/tasks/assigned-to-me/` | Get tasks assigned to user |
| GET    | `/api/tasks/reviewing/`      | Get tasks user reviews     |
| POST   | `/api/tasks/`                | Create a new task          |
| PATCH  | `/api/tasks/{task_id}/`      | Update a task              |
| DELETE | `/api/tasks/{task_id}/`      | Delete a task              |

---

### Comments

| Method | Endpoint                                      | Description              |
| ------ | --------------------------------------------- | ------------------------ |
| GET    | `/api/tasks/{task_id}/comments/`              | List comments for a task |
| POST   | `/api/tasks/{task_id}/comments/`              | Add comment to a task    |
| DELETE | `/api/tasks/{task_id}/comments/{comment_id}/` | Remove a comment         |

---

## Project Structure

```
/apps
  /app_auth
  /app_boards
  /app_tasks
/config
manage.py
```

Each app follows a simple structure:

```
api/
  serializers.py
  views.py
  urls.py
models.py
```

---

## Features

* User registration & login (token-based)
* Board creation and member management
* Task assignment and review workflow
* Comment system for tasks
* Permission handling (board membership, ownership)

---
