# Kanmind Backend (Django + DRF)

This project is a backend API for a Kanban board application.
It provides authentication, board management, task handling, and commenting features.

The frontend is provided separately and communicates with this API via REST endpoints.

---

## 🚀 Tech Stack

* Python
* Django
* Django REST Framework
* Token Authentication

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/AlexPutilin/KanMind.git
cd KanMind
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

---

## 🔐 Authentication

Token-based authentication is used.

After login or registration, include the token in requests:

```
Authorization: Token <your_token>
```

---

## 📡 API Endpoints

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

## 🧠 Project Structure

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

## ✅ Features

* User registration & login (token-based)
* Board creation and member management
* Task assignment and review workflow
* Comment system for tasks
* Permission handling (board membership, ownership)

---

## 📄 License

This project is for educational purposes.
