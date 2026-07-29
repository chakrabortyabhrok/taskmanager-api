# Task Manager API

A production-ready RESTful API for managing tasks, built with Django and Django REST Framework.  
The project includes JWT authentication, advanced filtering, AI-powered features, and full Docker support.

**Live Demo:** [https://taskmanager-api-d57o.onrender.com](https://taskmanager-api-d57o.onrender.com)

---

## Features

- Full CRUD operations for Tasks
- Category management with ForeignKey relationship
- JWT Authentication (Register, Login, Token Refresh)
- Filtering by status and category
- Search functionality
- Pagination
- AI Task Summarization (OpenAI)
- Natural Language Query endpoint (`/api/tasks/ask_ai/`)
- Auto-categorization of tasks using AI
- PostgreSQL database
- Fully Dockerized (Docker + Docker Compose)
- Environment-based configuration

---

## Tech Stack

| Category          | Technology                          |
|-------------------|-------------------------------------|
| Backend           | Django 6, Django REST Framework     |
| Authentication    | djangorestframework-simplejwt       |
| Database          | PostgreSQL                          |
| AI                | OpenAI API (gpt-4o-mini)            |
| Containerization  | Docker, Docker Compose              |
| Filtering         | django-filter                       |
| Server            | Gunicorn                            |

---

## Project Structure

```bash
taskmanager-api/
├── core/                  # Main app (models, views, serializers, AI utils)
├── taskmanager_api/       # Project settings and URLs
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── manage.py

### 1. Clone the repository

```bash
git clone <https://github.com/chakrabortyabhrok/taskmanager-api.git>
cd taskmanager-api
```

### 2. Create virtual environment

```bash
python -m venv env
source env/bin/activate          
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

- Create a .env file in the project root and add the following:

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```
### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```



