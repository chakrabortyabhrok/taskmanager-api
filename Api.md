# API Documentation

Base URL (Local): `http://localhost:8000`  
Base URL (Live): `https://taskmanager-api-d57o.onrender.com`

All protected endpoints require a valid JWT Access Token in the header:

```http
Authorization: Bearer <access_token>
```
## Authentication Endpoints
1. Register
- Method: POST
- URL: /api/auth/register/
- Auth Required: No

Request Body:
```bash
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "strongpassword123"
}
```
Success Response (201):
```bash
{
  "message": "User registered successfully"
}
```

2. Login
- Method: POST
- URL: /api/auth/login/
- Auth Required: No

Request Body:
```bash
{
  "username": "testuser",
  "password": "strongpassword123"
}
```
Success Response (200):
```bash
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

3. Refresh Token
- Method: POST
- URL: /api/auth/token/refresh/
- Auth Required: No

Request body:
```bash
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
Success Response (200):
```bash
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
## Task Endpoints
4. List Tasks
- Method: GET
- URL: /api/tasks/
- Auth Required: Yes

## Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `status` | Filter by status | `?status=todo` |
| `category` | Filter by category name | `?category=Work` |
| `search` | Search in title and description | `?search=meeting` |
| `ordering` | Order results | `?ordering=-created_at` |
| `page` | Pagination | `?page=2` |

Success Response (200):
```bash
{
  "count": 12,
  "next": "http://localhost:8000/api/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Fix dashboard bug",
      "description": "Resolve profile picture upload error",
      "status": "in_progress",
      "category": "Engineering",
      "due_date": null,
      "created_at": "2026-07-20T10:30:00Z",
      "updated_at": "2026-07-20T10:30:00Z",
      "ai_summary": "Fix the profile picture upload issue on the dashboard."
    }
  ]
}
```

5. Create Task
- Method: POST
- URL: /api/tasks/
- Auth Required: Yes

Request Body:
```bash
{
  "title": "Prepare project presentation",
  "description": "Create slides for the client meeting next week",
  "status": "todo",
  "due_date": "2026-08-05T18:00:00Z"
}
```
Success Response (201):
```bash
{
  "id": 15,
  "title": "Prepare project presentation",
  "description": "Create slides for the client meeting next week",
  "status": "todo",
  "category": "Work",
  "due_date": "2026-08-05T18:00:00Z",
  "created_at": "2026-07-29T09:15:00Z",
  "updated_at": "2026-07-29T09:15:00Z",
  "ai_summary": "Create presentation slides for the upcoming client meeting."
}
```

6. Retrieve Single Task
- Method: GET
- URL: /api/tasks/{id}/
- Auth Required: Yes

Success Response (200):
```bash
{
  "id": 15,
  "title": "Prepare project presentation",
  "description": "Create slides for the client meeting next week",
  "status": "todo",
  "category": "Work",
  "due_date": "2026-08-05T18:00:00Z",
  "created_at": "2026-07-29T09:15:00Z",
  "updated_at": "2026-07-29T09:15:00Z",
  "ai_summary": "Create presentation slides for the upcoming client meeting."
}
```

7. Update Task (Full)
- Method: PUT
- URL: /api/tasks/{id}/
- Auth Required: Yes

Request Body:
```bash
{
  "title": "Prepare project presentation",
  "description": "Updated description",
  "status": "in_progress",
  "due_date": "2026-08-05T18:00:00Z"
}
```

8. Partial Update Task
- Method: PATCH
- URL: /api/tasks/{id}/
- Auth Required: Yes

Request Body (example):
```bash
{
  "status": "done"
}
```

9. Delete Task

Method: DELETE
URL: /api/tasks/{id}/
Auth Required: Yes

Success Response: 204 No Content

## AI Endpoints
10. Ask AI about Tasks
- Method: POST
- URL: /api/tasks/ask_ai/
- Auth Required: Yes

Request Body:
```bash
{
  "question": "Which tasks are currently in progress?"
}
```

Success Response (200)
```bash
{
  "answer": "You currently have 3 tasks in progress: Fix dashboard bug, Prepare project presentation, and Update monthly budget spreadsheet."
}
```

## Possible Error Responses

| Status Code | Meaning | Example Message |
|-------------|---------|-----------------|
| `400` | Bad Request | Validation errors / missing fields |
| `401` | Unauthorized | Authentication credentials were not provided |
| `403` | Forbidden | You do not have permission |
| `404` | Not Found | Task not found |
| `500` | Internal Server Error | Unexpected server error |