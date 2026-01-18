# Full-Stack Integration Guide

How the 5 skills work together to build a complete application.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│                   nextjs-app-router skill                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ App Router  │  │   Server    │  │  Client Components  │  │
│  │   Pages     │  │  Components │  │   (React hooks)     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          └────────────────┼────────────────────┘
                           │ HTTP/REST
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│                   fastapi-backend skill                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Endpoints  │  │  Pydantic   │  │    Dependencies     │  │
│  │  (routes)   │  │   Models    │  │   (get_session)     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          └────────────────┼────────────────────┘
                           │ SQLModel ORM
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   ORM Layer (SQLModel)                       │
│                    sqlmodel-orm skill                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Models    │  │   Session   │  │    Relationships    │  │
│  │  (tables)   │  │  Management │  │   (foreign keys)    │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          └────────────────┼────────────────────┘
                           │ PostgreSQL Protocol
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Database (Neon PostgreSQL)                  │
│                      neon-db skill                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Tables    │  │  Branches   │  │   Connection Pool   │  │
│  │   (data)    │  │  (dev/prod) │  │     (pooler)        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

                    Testing Layer (pytest)
                     pytest-tdd skill
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Unit Tests  │  │ Integration │  │   Test Fixtures     │  │
│  │             │  │   Tests     │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Project Setup Sequence

### 1. Database Setup (neon-db)

```bash
# Create Neon project and get connection string
# Add to .env
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/db?sslmode=require
```

### 2. Backend Setup (fastapi-backend + sqlmodel-orm)

```bash
# Create backend directory
mkdir backend && cd backend

# Initialize FastAPI project
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlmodel python-dotenv

# Create main.py with SQLModel integration
```

```python
# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine
from contextlib import asynccontextmanager
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session
```

### 3. Frontend Setup (nextjs-app-router)

```bash
# Create Next.js app
npx create-next-app@latest frontend --typescript --tailwind --app

# Add environment variable
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
```

```typescript
// frontend/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL

export async function fetchTodos() {
  const res = await fetch(`${API_URL}/todos`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Failed to fetch')
  return res.json()
}
```

### 4. Testing Setup (pytest-tdd)

```bash
# Install test dependencies
pip install pytest pytest-cov httpx

# Create pytest.ini
cat > pytest.ini << EOF
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
EOF
```

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from backend.main import app, get_session

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
```

## Complete Example: Todo Feature

### 1. Define Model (sqlmodel-orm)

```python
# backend/models.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TodoBase(SQLModel):
    title: str
    completed: bool = False

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    created_at: datetime
```

### 2. Create API Endpoints (fastapi-backend)

```python
# backend/routes/todos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Todo, TodoCreate, TodoRead
from main import get_session

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=list[TodoRead])
def get_todos(session: Session = Depends(get_session)):
    return session.exec(select(Todo)).all()

@router.post("/", response_model=TodoRead, status_code=201)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@router.patch("/{todo_id}", response_model=TodoRead)
def update_todo(todo_id: int, completed: bool, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = completed
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
```

### 3. Build Frontend (nextjs-app-router)

```typescript
// frontend/app/page.tsx
import { TodoList } from '@/components/TodoList'

async function getTodos() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/todos`, {
    cache: 'no-store'
  })
  if (!res.ok) throw new Error('Failed to fetch todos')
  return res.json()
}

export default async function Home() {
  const todos = await getTodos()
  return <TodoList initialTodos={todos} />
}
```

```typescript
// frontend/components/TodoList.tsx
'use client'
import { useState } from 'react'

interface Todo {
  id: number
  title: string
  completed: boolean
}

export function TodoList({ initialTodos }: { initialTodos: Todo[] }) {
  const [todos, setTodos] = useState(initialTodos)
  const [newTitle, setNewTitle] = useState('')

  async function addTodo() {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTitle })
    })
    if (res.ok) {
      const todo = await res.json()
      setTodos([...todos, todo])
      setNewTitle('')
    }
  }

  async function toggleTodo(id: number, completed: boolean) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/todos/${id}?completed=${!completed}`, {
      method: 'PATCH'
    })
    if (res.ok) {
      setTodos(todos.map(t => t.id === id ? { ...t, completed: !completed } : t))
    }
  }

  return (
    <div className="p-4">
      <div className="flex gap-2 mb-4">
        <input
          value={newTitle}
          onChange={e => setNewTitle(e.target.value)}
          className="border p-2 rounded"
          placeholder="New todo..."
        />
        <button onClick={addTodo} className="bg-blue-500 text-white px-4 rounded">
          Add
        </button>
      </div>
      <ul>
        {todos.map(todo => (
          <li key={todo.id} className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id, todo.completed)}
            />
            <span className={todo.completed ? 'line-through' : ''}>
              {todo.title}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
```

### 4. Write Tests (pytest-tdd)

```python
# tests/test_todos.py
import pytest

def test_create_todo(client):
    response = client.post("/todos", json={"title": "Test todo"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["completed"] is False
    assert "id" in data

def test_get_todos(client, session):
    # Arrange
    from models import Todo
    todo = Todo(title="Existing todo")
    session.add(todo)
    session.commit()

    # Act
    response = client.get("/todos")

    # Assert
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Existing todo"

def test_toggle_todo(client, session):
    from models import Todo
    todo = Todo(title="Toggle me")
    session.add(todo)
    session.commit()

    response = client.patch(f"/todos/{todo.id}?completed=true")
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_delete_todo(client, session):
    from models import Todo
    todo = Todo(title="Delete me")
    session.add(todo)
    session.commit()

    response = client.delete(f"/todos/{todo.id}")
    assert response.status_code == 204

    # Verify deleted
    response = client.get("/todos")
    assert len(response.json()) == 0

def test_todo_not_found(client):
    response = client.patch("/todos/9999?completed=true")
    assert response.status_code == 404
```

## Environment Configuration

### Development (.env.local)

```bash
# Backend
DATABASE_URL=postgresql://user:pass@ep-dev.neon.tech/db?sslmode=require

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production (.env.production)

```bash
# Backend
DATABASE_URL=postgresql://user:pass@ep-prod.neon.tech/db?sslmode=require

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourapp.com
```

## Running the Stack

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Tests
cd backend
pytest --cov=. --cov-report=term-missing
```

## Common Integration Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| CORS errors | Missing middleware | Add CORSMiddleware with frontend URL |
| 422 errors | Schema mismatch | Check Pydantic model matches request |
| Connection refused | Backend not running | Start uvicorn first |
| Hydration mismatch | Server/client differ | Use 'use client' for dynamic data |
| Tests fail in CI | No test database | Use SQLite in-memory for tests |

## Skill Reference Quick Links

- **pytest-tdd**: Test patterns, fixtures, TDD workflow
- **fastapi-backend**: Endpoints, middleware, dependencies
- **sqlmodel-orm**: Models, relationships, queries
- **neon-db**: Connection, branches, pooling
- **nextjs-app-router**: Components, routing, data fetching
