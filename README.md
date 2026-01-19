# Todo Application - Phase II

A modern full-stack todo application with user authentication, built with Next.js and FastAPI.

## Live Demo

- **Frontend**: [Vercel Deployment](https://your-app.vercel.app) *(Update with your Vercel URL)*
- **API Docs**: [Swagger UI](https://your-backend.railway.app/docs) *(Update with your backend URL)*

## Features

- User Authentication (Sign Up / Sign In)
- Create, Read, Update, Delete Todos
- Mark todos as complete/active
- Search and filter todos
- Modern Facebook-style UI
- Responsive design

## Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Inline Styles
- **Auth**: JWT with localStorage

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon)
- **Auth**: JWT with bcrypt password hashing

## Project Structure

```
hacathon_02/
├── frontend/          # Next.js frontend application
│   ├── app/           # App router pages
│   ├── lib/           # Utilities and API client
│   └── public/        # Static assets
├── backend/           # FastAPI backend application
│   ├── routers/       # API route handlers
│   ├── models/        # Database models
│   └── main.py        # Application entry point
└── tests/             # Test suites
```

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL (or Neon account)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configure your database URL
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local  # Configure API URL
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/sign-up` - Register new user
- `POST /api/auth/sign-in` - Login user
- `GET /api/auth/me` - Get current user

### Todos
- `GET /api/todos/` - List all todos
- `POST /api/todos/` - Create todo
- `GET /api/todos/{id}` - Get todo by ID
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo

## Screenshots

### Sign In Page
Facebook-style login with email/password authentication.

### Todo Dashboard
View all your todos with stats, search, and filters.

### Create Todo
Simple form to add new tasks with title and description.

## Development

```bash
# Run backend tests
cd backend && pytest

# Run frontend build
cd frontend && npm run build
```

## Deployment

- **Frontend**: Deploy to Vercel (auto-detects Next.js)
- **Backend**: Deploy to Railway, Render, or Fly.io

## Phase I vs Phase II

| Feature | Phase I | Phase II |
|---------|---------|----------|
| Interface | CLI Menu | Web UI |
| Storage | In-memory | PostgreSQL |
| Auth | None | JWT |
| Tech | Python only | Next.js + FastAPI |

---

Built with Next.js, FastAPI, and PostgreSQL
