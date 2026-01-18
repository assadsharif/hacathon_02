# Phase II Tasks — Hackathon II

## Task Group A: Backend

A1. Create FastAPI project skeleton
A2. Define SQLModel Todo schema
A3. Configure Neon DB connection
A4. Implement CRUD endpoints
A5. Validate parity with Phase I rules

## Task Group B: Frontend

B1. Initialize Next.js App Router
B2. Define API client layer
B3. Create Todo pages (list, create, update)
   - List view: Display all todos with filter by status
   - Create form: Title input + submit
   - Update form: Edit title and status
B4. Implement delete UI and confirmation
   - Delete button with confirmation dialog
   - Optimistic UI updates
B5. Handle loading & error states
   - Loading spinner during API calls
   - Error toast/message for network failures
   - Validation error display (inline form errors)

## Task Group C: Integration

C1. Connect frontend to backend
C2. Validate full CRUD flow
C3. Cross-check behavior vs Phase I

## Task Group D: Deployment Setup

D1. Create environment configuration
   - Create `.env.example` with DATABASE_URL template
   - Document required environment variables
   - Add .env to .gitignore
D2. Document local setup
   - README with installation steps
   - Database setup instructions (Neon)
   - Run commands (backend + frontend)
D3. Create development tooling (optional)
   - docker-compose for local Postgres (Neon alternative)
   - Dev scripts (start backend, start frontend)

## Task Discipline
- One task at a time
- Specs referenced in every task
- No task expands scope
