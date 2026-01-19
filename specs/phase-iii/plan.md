# Phase III Plan — AI Integration

## Strategy
Wrap existing Phase II backend with an AI-controlled conversational layer.

## Milestones

### M1: Tool Definition
- Map Phase II APIs to MCP tools
- Freeze tool contracts

### M2: Agent Design
- Single TodoAgent
- Tool-first execution
- Deterministic responses

### M3: Chat UI
- ChatKit UI integration
- Message streaming
- Error visibility

### M4: End-to-End Validation
- Chat → Agent → Tool → API → DB → Response
- Parity checks with Phase II UI

## Risk Controls
- Tool-only execution
- No prompt-based logic
- Clear refusal paths

## Completion Criteria
- Chatbot performs full CRUD
- All actions traceable
- No regression in Phase II

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    PHASE III (NEW)                        │
│                                                          │
│  ┌────────────────┐    ┌────────────────────────────┐   │
│  │   ChatKit UI   │───▶│      TodoAgent             │   │
│  │  (Messages)    │    │  - Interprets intent       │   │
│  └────────────────┘    │  - Selects tool            │   │
│                        │  - Returns response        │   │
│                        └─────────────┬──────────────┘   │
│                                      │                   │
│                        ┌─────────────▼──────────────┐   │
│                        │      MCP Tools             │   │
│                        │  create_todo | list_todos  │   │
│                        │  get_todo | update_todo    │   │
│                        │  delete_todo               │   │
│                        └─────────────┬──────────────┘   │
└──────────────────────────────────────┼───────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────┐
│              PHASE II (UNCHANGED)                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │            FastAPI Backend                       │    │
│  │  POST/GET/PUT/DELETE /api/todos                 │    │
│  └─────────────────────┬───────────────────────────┘    │
│                        │                                 │
│  ┌─────────────────────▼───────────────────────────┐    │
│  │            PostgreSQL (Neon)                     │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Message
    │
    ▼
┌─────────────┐
│  ChatKit UI │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  TodoAgent  │──── Intent Recognition
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  MCP Tool   │──── Parameter Extraction
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Phase II   │──── API Call (with JWT)
│  Backend    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Response   │──── Formatted for User
└─────────────┘
```

## Tool Contracts (Frozen)

| Tool | Input | Output |
|------|-------|--------|
| `create_todo` | title, description? | Todo object |
| `list_todos` | status? | Todo[] |
| `get_todo` | id | Todo |
| `update_todo` | id, title?, description?, status? | Todo |
| `delete_todo` | id | Success message |

## Environment Requirements

```bash
# New variables for Phase III
OPENAI_API_KEY=sk-...
```

## File Structure

```
frontend/
├── app/
│   └── chat/
│       └── page.tsx       # Chat interface
├── components/
│   └── chat/
│       ├── ChatWindow.tsx
│       ├── MessageList.tsx
│       └── ChatInput.tsx
└── lib/
    └── agent/
        ├── TodoAgent.ts   # Agent logic
        └── tools.ts       # MCP tool definitions
```
