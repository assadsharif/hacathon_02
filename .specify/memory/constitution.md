# Hackathon II Constitution

## Purpose

Define the architectural, technical, and governance principles for the Hackathon II project, which evolves a Phase I console Todo application into a Phase II full-stack web application while maintaining Phase I as the authoritative reference behavior.

## Core Principles

### I. Two-Phase Architecture (NON-NEGOTIABLE)

**Phase I: Console/In-Memory Foundation**
- Python-based console application with in-memory storage
- Defines the canonical domain logic and behavior
- Status: READ ONLY - serves as reference implementation
- Location: `specs/phase-i/` and existing implementation

**Phase II: Full-Stack Web Extension**
- Extends Phase I concepts into persistent, web-based architecture
- Must preserve Phase I domain logic and behavior exactly
- Location: `specs/phase-ii/` and new implementation
- Phase I directory MUST remain untouched during Phase II development

**Authority Order:**
1. Phase I Specifications (Highest Authority)
2. This Constitution
3. Phase II Specification (specify.md)
4. Phase II Plan (plan.md)
5. Phase II Tasks (tasks.md)
6. Phase II Implementation (Lowest Authority)

**Rationale:** Phase I establishes the "source of truth" for domain behavior. Phase II must prove compatibility through validation against Phase I, not redefine it.

### II. Technology Lock (NON-NEGOTIABLE)

**Phase I Stack:**
- Language: Python
- Storage: In-memory
- Interface: Console/CLI

**Phase II Stack:**
- Frontend: Next.js with App Router
- Backend: FastAPI (Python)
- ORM: SQLModel
- Database: Neon (PostgreSQL)
- Auth: Better Auth with JWT (user-scoped data)
- Deployment: Local-first, cloud-ready

**Rationale:** Technology decisions are frozen to prevent analysis paralysis. Focus is on execution, not exploration.

### III. Spec-Driven Development (SDD) - NON-NEGOTIABLE

**Mandatory Workflow:**
1. Specification → Plan → Tasks → Implementation
2. No coding before specs are approved
3. All implementation decisions must trace back to specs
4. Changes to behavior require spec amendments first

**Anti-Patterns (Forbidden):**
- Vibe coding (implementing without spec reference)
- Inline architecture decisions during implementation
- Skipping `/sp.*` workflow steps
- Silent refactors that change behavior

**Rationale:** Prevents scope creep, ensures traceability, enables reversal, maintains team alignment.

### IV. Test-First Development

**Requirements:**
- Tests written before implementation (Red-Green-Refactor)
- User approval of tests before implementation begins
- Phase II tests must validate parity with Phase I behavior
- All CRUD operations require integration tests

**Coverage Targets:**
- Backend endpoints: 100% happy path + error cases
- Frontend components: User interaction flows
- Integration: Full CRUD cycle end-to-end

**Rationale:** Tests serve as executable specifications and prevent regressions.

### V. Behavioral Compatibility

**Phase II Success Criteria:**
1. Phase I still runs independently (unmodified)
2. Web UI fully replaces console usage
3. Backend mirrors Phase I domain logic exactly
4. Database persistence works end-to-end
5. Same input → Same output (deterministic behavior)

**Validation Method:**
- Cross-check Phase II behavior against Phase I for all CRUD operations
- Document any divergence with explicit justification

**Rationale:** Phase II is an evolution, not a rewrite. Preserving Phase I ensures we don't lose validated functionality.

### VI. Simplicity and Focus

**Explicit Non-Goals:**
- AI features
- Real-time synchronization
- Background jobs/workers
- UI polish beyond functional MVP
- OAuth/SSO providers (using Better Auth email/password only)

**Constraints:**
- Smallest viable change
- No unrelated refactors
- YAGNI: Don't build for hypothetical future requirements
- One feature at a time

**Rationale:** Hackathon constraints demand ruthless prioritization. Ship working software over perfect software.

### VII. Observability and Debuggability

**Requirements:**
- RESTful endpoints with proper HTTP semantics
- Structured error responses (status codes, messages)
- Environment-based configuration (.env files)
- Clear separation of concerns (API client layer, service layer, data layer)

**Logging:**
- FastAPI default logging (no custom complexity)
- Log all database operations
- Log API request/response for debugging

**Rationale:** Simple observability enables fast debugging without additional tooling.

### VIII. Authentication and Security

**Authentication Strategy:**
- **Provider:** Better Auth (official Next.js-compatible library)
- **Token Type:** JWT (JSON Web Tokens)
- **JWT Secret:** Managed via environment variables (never hardcoded)
- **Session Storage:** Database-backed (not in-memory)
- **Login Page:** `/sign-in` (standard Better Auth convention)

**Security Principles:**
1. **User-Scoped Data:** All todos MUST be filtered by authenticated user ID
2. **JWT Verification:** Backend MUST verify JWT on every protected endpoint
3. **Token Transmission:** JWT sent via Authorization header (`Bearer <token>`)
4. **No Anonymous Access:** All todo operations require authentication
5. **Password Security:** Better Auth handles hashing (bcrypt/argon2)

**Data Isolation:**
- Each user sees ONLY their own todos
- Database queries MUST include `WHERE user_id = <authenticated_user_id>`
- No shared/public todos in this phase
- User ID extracted from verified JWT claims

**Implementation Requirements:**
1. Frontend: Better Auth client with MCP plugin for login page
2. Frontend API Client: Attach JWT to all requests automatically
3. Backend: FastAPI middleware to verify JWT and extract user_id
4. Database: Add `user_id` foreign key to todos table
5. API Routes: Filter all queries by authenticated user

**Explicit Non-Goals:**
- OAuth providers (Google, GitHub) - keep auth simple
- Multi-factor authentication (MFA)
- Password reset flows (Phase III feature)
- Role-based access control (RBAC) - single user role only
- Session refresh/rotation (use Better Auth defaults)

**JWT Configuration:**
- Algorithm: HS256 (symmetric signing)
- Expiration: 7 days (Better Auth default)
- Claims: `user_id`, `email`, `iat`, `exp`
- Secret Key: 256-bit minimum (provided: `93457b5f5d59fd9d65726648e22a4e28`)

**Rationale:** Better Auth provides production-ready authentication without OAuth complexity. JWT enables stateless authentication suitable for serverless backends. User-scoped data ensures security and privacy by design.

## Development Workflow

### Specification Process
1. User provides feature description
2. `/sp.specify`: Create or update `specs/phase-ii/specify.md`
3. `/sp.plan`: Generate architectural plan in `specs/phase-ii/plan.md`
4. `/sp.tasks`: Break down into testable tasks in `specs/phase-ii/tasks.md`
5. User approves specs before implementation begins

### Implementation Process
1. One task at a time (no parallelization without explicit approval)
2. Reference spec/plan/task in commit messages
3. Run tests after each task completion
4. Update `implement.md` with progress

### Quality Gates
- All tests pass before marking task complete
- No unresolved TODOs in committed code
- All environment variables documented in `.env.example`
- Phase I validation tests pass for Phase II features

## Architectural Decision Records (ADR)

**When to Create ADR:**
Test for significance (ALL must be true):
1. **Impact:** Long-term consequences (framework, data model, API design, security, platform)
2. **Alternatives:** Multiple viable options were considered
3. **Scope:** Decision is cross-cutting and influences system design

**Process:**
- Architect/agent suggests ADR with brief summary
- User approves creation
- Document using `/sp.adr <decision-title>`
- Store in `history/adr/`

**Never Auto-Create:** ADRs require explicit user consent.

## Prompt History Records (PHR)

**Mandatory Recording:**
After every significant user interaction:
1. Implementation work (code changes, features)
2. Planning/architecture discussions
3. Debugging sessions
4. Spec/task/plan creation

**Routing (all under `history/prompts/`):**
- Constitution work → `history/prompts/constitution/`
- Feature stages (spec, plan, tasks, implementation) → `history/prompts/<feature-name>/`
- General queries → `history/prompts/general/`

**Process:**
- Use agent-native flow (read template, fill placeholders, write file)
- Preserve full user input (verbatim, no truncation)
- Record key assistant output
- Validate: no unresolved placeholders, correct path

## Governance

### Constitution Authority
- This constitution supersedes all other practices
- Amendments require explicit user approval and version bump
- All code changes must comply with constitution principles

### Versioning
- **Version Format:** MAJOR.MINOR.PATCH
- **MAJOR:** Backward-incompatible principle changes
- **MINOR:** New principles or material guidance expansions
- **PATCH:** Clarifications, typos, non-semantic refinements

### Compliance
- All PRs/commits must reference specs
- Architecture changes require ADR
- Test-first violations require immediate correction
- Constitution violations block merge

### Amendment Process
1. Propose change with rationale
2. Document impact on existing specs/code
3. User approval required
4. Update version and last-amended date
5. Propagate changes to dependent templates

---

**Version:** 1.1.0
**Ratified:** 2026-01-11
**Last Amended:** 2026-01-12
**Amendment:** Added Section VIII - Authentication and Security (Better Auth + JWT)
