# Phase II - Full-Stack Web Todo Application

Transform the Phase I console Todo application into a full-stack web application with Next.js frontend, FastAPI backend, and Neon PostgreSQL database.

## Technology Stack

- **Frontend**: Next.js 14+ (App Router)
- **Backend**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL (Serverless)
- **Language**: Python 3.13+, TypeScript

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ and npm/yarn installed
- Neon account and database project ([neon.tech](https://neon.tech))
- Git

## Database Setup (Neon)

### 1. Get Your Neon Connection String

Your Neon connection string is already configured in `.env`:
```
postgresql://neondb_owner:npg_bEMG4OHC3ukS@ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

**Connection Details:**
- **Host**: `ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech`
- **Database**: `neondb`
- **User**: `neondb_owner`
- **Region**: `ap-southeast-1` (Singapore)
- **Connection Type**: Pooled (using pgBouncer)

### 2. Environment Variables

The project uses environment variables for configuration:

```bash
# .env (DO NOT commit this file)
DATABASE_URL=postgresql://neondb_owner:npg_bEMG4OHC3ukS@ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
ENVIRONMENT=development
DEBUG=True
```

**Note**: `.env` is already in `.gitignore` to protect credentials.

### 3. Verify Connection

You can test the database connection using:

```bash
# Using psql (if installed)
psql 'postgresql://neondb_owner:npg_bEMG4OHC3ukS@ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# Or use Python script (to be created)
python scripts/verify_db_connection.py
```

## Project Structure (To Be Created)

```
.
├── backend/                 # FastAPI backend
│   ├── main.py             # FastAPI app entry point
│   ├── database.py         # Database connection & session
│   ├── models.py           # SQLModel table definitions
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── routers/            # API route handlers
│   │   └── todos.py
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Next.js frontend
│   ├── app/                # App Router directory
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Home page
│   │   ├── todos/          # Todo pages
│   │   │   ├── page.tsx    # List todos
│   │   │   ├── create/
│   │   │   └── [id]/
│   │   └── api/            # API routes (optional)
│   ├── components/         # React components
│   ├── lib/                # Utilities
│   │   └── api.ts          # API client for backend
│   ├── types/              # TypeScript types
│   ├── package.json
│   └── tsconfig.json
│
├── specs/                  # Specifications
│   ├── phase-i/            # Phase I (READ ONLY)
│   └── phase-ii/           # Phase II (current)
│       ├── specify.md
│       ├── plan.md
│       ├── tasks.md
│       └── implement.md
│
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example            # Environment template (COMMIT THIS)
└── README.md              # This file
```

## Installation & Setup

### Backend Setup

```bash
# Navigate to backend directory (to be created)
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlmodel psycopg2-binary python-dotenv

# Create requirements.txt
pip freeze > requirements.txt

# Run database migrations (create tables)
python -c "from database import create_db_and_tables; create_db_and_tables()"

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at**: http://localhost:8000
**API Documentation**: http://localhost:8000/docs (Swagger UI)

### Frontend Setup

```bash
# Navigate to frontend directory (to be created)
cd frontend

# Install dependencies
npm install
# or
yarn install

# Start development server
npm run dev
# or
yarn dev
```

**Frontend will be available at**: http://localhost:3000

## Development Workflow

### 1. Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 2. Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

### 3. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Database Management

### View Database (Neon Console)

1. Visit [Neon Console](https://console.neon.tech)
2. Select your project
3. Go to "Tables" or "SQL Editor"

### Create Tables

Tables are automatically created on backend startup using SQLModel:

```python
# backend/database.py
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)  # Creates all tables
```

### Run Migrations (Optional)

For production, use Alembic:

```bash
cd backend
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## API Endpoints (To Be Implemented)

### Todos

- `GET /api/todos` - List all todos (with optional status filter)
- `GET /api/todos/{id}` - Get single todo
- `POST /api/todos` - Create todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo

### Health Check

- `GET /` - API root
- `GET /health` - Health check
- `GET /health/db` - Database connectivity check

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
# or
yarn test
```

## Environment Configuration

### Development

```bash
# .env (already configured)
DATABASE_URL=postgresql://neondb_owner:npg_bEMG4OHC3ukS@ep-bold-heart-a1ehngm7-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
ENVIRONMENT=development
DEBUG=True
```

### Production

For production deployment, update `.env.production`:

```bash
DATABASE_URL=<production-neon-connection-string>
ENVIRONMENT=production
DEBUG=False
```

## Troubleshooting

### Database Connection Issues

**Error**: `connection to server failed`

**Solutions**:
1. Verify DATABASE_URL is correct in `.env`
2. Check network connectivity
3. Ensure SSL mode is enabled (`?sslmode=require`)
4. Verify Neon project is active

**Test Connection**:
```bash
psql '<your-connection-string>'
```

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**: Change port or kill existing process:
```bash
# Backend: Use different port
uvicorn main:app --reload --port 8001

# Frontend: Use different port
npm run dev -- -p 3001
```

## Phase I Reference

Phase I (console application) remains **READ ONLY** in `specs/phase-i/` and the existing `src/` directory. It serves as the reference implementation for Phase II behavior validation.

**Do NOT modify Phase I code.** Phase II must prove behavioral compatibility through validation tests.

## Next Steps

See `implement.md` for current implementation status and next tasks.

**Current Task**: A1 - Create FastAPI project skeleton

## Resources

- [Phase II Specification](./specify.md)
- [Implementation Plan](./plan.md)
- [Task Breakdown](./tasks.md)
- [Implementation Log](./implement.md)
- [Neon Documentation](https://neon.tech/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
