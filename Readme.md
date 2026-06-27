# Task Manager API

A RESTful API built with Django and Django REST Framework that allows users to manage tasks with AI-powered features.

## Features

- CRUD operations for Tasks
- Category management
- Filtering, searching, and ordering support
- AI-generated task summaries (using OpenAI)
- Natural language query endpoint (ask questions about your tasks in plain English)

## Tech Stack

- Python
- Django
- Django REST Framework
- OpenAI API (gpt-4o-mini)
- PostgreSQL (Production)
- SQLite (Development)

## Local Setup

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



