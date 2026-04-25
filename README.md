# Daily Log (Activity Tracker)

## Overview

Daily Log is a simple full-stack web application for tracking daily entries. It allows users to create, view, update, and delete short notes or activities through a minimal interface.

The project is primarily built as a learning sandbox to explore backend development, database integration, and frontend–backend communication.

---

## Features

- Create daily entries with optional tags
- View all saved entries in reverse chronological order
- Edit existing entries
- Delete entries
- Lightweight, minimal UI
- REST API backend
- Persistent storage using SQLite

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy ORM
- SQLite database
- Pydantic (v2) for validation
- Uvicorn ASGI server

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript (Fetch API)

---

## Project Structure

```
daily-log/
├── app/ # FastAPI application
├── db/ # Database models and logic
├── frontend/ # Static frontend (HTML/CSS/JS)
├── daily_log.db # SQLite database file
├── pyproject.toml # Dependencies (uv/pip)
├── uv.lock
└── README.md
```


---

## API Endpoints


```
GET    /check          → health check
POST   /entries        → create entry  
GET    /entries        → list all entries  
PUT    /entries/{id}   → update entry  
DELETE /entries/{id}   → delete entry
```  

## Running the Project Locally

1. Start backend
```bash
uvicorn app.main:app --reload

# Backend runs at: http://127.0.0.1:8000
# API docs: http://127.0.0.1:8000/docs
```

2. Start frontend
```bash
cd frontend
python -m http.server 5500

# Frontend runs at: http://127.0.0.1:5500
```
---