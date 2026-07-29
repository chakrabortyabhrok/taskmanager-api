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
```

### 1. Clone the repository

```bash
git clone https://github.com/chakrabortyabhrok/taskmanager-api.git
cd taskmanager-api
```

### 2. Environment Variables
- Create a .env file in the root directory:

    ```bash
    # Django
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

    # PostgreSQL
    POSTGRES_DB=taskmanager_db
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_strong_password

    # OpenAI
    OPENAI_API_KEY=sk-your-openai-key          
    ```
    Note: Never commit the real .env file. A .env.example is provided.
  ### Running the Project
  Option 1: Using Docker (Recommended)
  ```bash
  docker compose up --build
  ```
  The API will probably be available at: http://localhost:8000

  Option 2: Local Development
  ```bash
  python -m venv env
  source env/bin/activate          # Windows: env\Scripts\activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver
  ```
  ###Authentication
  The API uses JWT Authentication.
  Register
  ```bash
  POST /api/auth/register/
  Content-Type: application/json

  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "strongpassword123"
  }
  ```
  Login
  ```bash
  POST /api/auth/login/
  Content-Type: application/json

  {
    "username": "testuser",
    "password": "strongpassword123"
  }
  ```
  Response:
  ```bash
  {
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
  Using the Access Token
  Add the token in the header of protected requests:
  ```bash
  Authorization: Bearer <your_access_token>
  ```
  Refresh Token
  ```bash
  POST /api/auth/token/refresh/
  Content-Type: application/json

  {
    "refresh": "<your_refresh_token>"
  }
  ```
  
  ---
  ## API Endpoints
  "Look for (Api.md) file in the root of the project, for more detailed API Documentation"
  Tasks
  | Method | Endpoint | Description | Auth Required |
  |--------|----------|-------------|---------------|
  | `GET` | `/api/tasks/` | List all tasks | Yes |
  | `POST` | `/api/tasks/` | Create a new task | Yes |
  | `GET` | `/api/tasks/{id}/` | Retrieve a single task | Yes |
  | `PUT` | `/api/tasks/{id}/` | Update a task (full) | Yes |
  | `PATCH` | `/api/tasks/{id}/` | Partial update | Yes |
  | `DELETE` | `/api/tasks/{id}/` | Delete a task | Yes |
  | `POST` | `/api/tasks/ask_ai/` | Ask questions about tasks | Yes |
  ---

  Filtering & Search Examples
  
  ```bash
  GET /api/tasks/?status=todo
  GET /api/tasks/?category=Work
  GET /api/tasks/?search=meeting
  GET /api/tasks/?ordering=-created_at
  GET /api/tasks/?page=2
  ```
  AI Features
  1. AI Task Summarization
     When a task is created or updated, an AI-generated summary is automatically stored in the ai_summary field.
  2. Natural Language Queries
     You can ask questions about your tasks in plain English:
     
     ```bash
     POST /api/tasks/ask_ai/
     Authorization: Bearer <token>
     Content-Type: application/json

     {
       "question": "Which tasks are currently in progress?"
     }
     ```
  3. Auto-Categorization
     When creating a task, the system can automatically suggest a suitable category using AI.
     
     Environment Variables

    | Variable | Description | Required |
    |----------|-------------|----------|
    | `SECRET_KEY` | Django secret key | Yes |
    | `DEBUG` | Debug mode (`True` / `False`) | Yes |
    | `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Yes |
    | `POSTGRES_DB` | PostgreSQL database name | Yes |
    | `POSTGRES_USER` | PostgreSQL username | Yes |
    | `POSTGRES_PASSWORD` | PostgreSQL password | Yes |
    | `OPENAI_API_KEY` | OpenAI API key | Yes |

## Future Improvements

  - User-specific tasks (task ownership)
  - Role-based permissions
  - Rate limiting on AI endpoints
  - Caching AI responses
  - Frontend dashboard with React
  - Automated tests with higher coverage
  - CI/CD pipeline

## Author
### Abhrok Chakraborty
Self-taught developer focused on building production-ready backend systems with Django, DRF, and AI integration.

## License
This project is open source and available under the MIT License.