# Phase III Tasks — AI Chatbot

## Task Group A: Tool Layer
A1. Define MCP tools for each API endpoint
A2. Validate tool schemas
A3. Freeze tool contracts

## Task Group B: Agent
B1. Define TodoAgent role
B2. Bind tools to agent
B3. Define refusal and clarification logic

## Task Group C: Chat UI
C1. Integrate OpenAI ChatKit
C2. Connect to Agent SDK
C3. Display structured responses

## Task Group D: Validation
D1. CRUD via chat validation
D2. Error handling tests
D3. Phase II parity checks

## Task Discipline
- One task at a time
- No cross-task leakage
- Specs referenced explicitly

---

## Task Details

### Task Group A: Tool Layer

| Task | Description | Deliverable |
|------|-------------|-------------|
| A1 | Define MCP tools for create_todo, list_todos, get_todo, update_todo, delete_todo | `lib/agent/tools.ts` |
| A2 | Validate tool schemas match Phase II API contracts | Test script |
| A3 | Freeze tool contracts - no changes after this | Documented contracts |

### Task Group B: Agent

| Task | Description | Deliverable |
|------|-------------|-------------|
| B1 | Define TodoAgent with system prompt and role | `lib/agent/TodoAgent.ts` |
| B2 | Bind MCP tools to agent | Agent configuration |
| B3 | Implement refusal for unsupported requests, clarification for ambiguous | Logic in agent |

### Task Group C: Chat UI

| Task | Description | Deliverable |
|------|-------------|-------------|
| C1 | Add ChatKit components to frontend | `components/chat/*` |
| C2 | Connect ChatKit to TodoAgent via SDK | Integration code |
| C3 | Display tool invocations and formatted responses | UI components |

### Task Group D: Validation

| Task | Description | Deliverable |
|------|-------------|-------------|
| D1 | Test: Create, List, Update, Delete via chat | Test results |
| D2 | Test: Error messages, auth failures, not found | Test results |
| D3 | Verify Phase II UI still works, no regressions | Test results |

---

## Acceptance Criteria

### A1: MCP Tools Defined
- [ ] `create_todo` tool calls POST /api/todos
- [ ] `list_todos` tool calls GET /api/todos
- [ ] `get_todo` tool calls GET /api/todos/{id}
- [ ] `update_todo` tool calls PUT /api/todos/{id}
- [ ] `delete_todo` tool calls DELETE /api/todos/{id}
- [ ] All tools pass JWT token

### B1: TodoAgent Role
- [ ] System prompt defines todo management scope
- [ ] Agent uses tools for all mutations
- [ ] Agent never invents data

### B3: Refusal & Clarification
- [ ] "Schedule tasks" → Refused with explanation
- [ ] "Delete it" (no context) → Asks for clarification
- [ ] Unsupported actions → Clear refusal message

### C3: Structured Responses
- [ ] Tool invocations visible (toggle)
- [ ] Todo lists formatted as numbered list
- [ ] Success/error messages clear

### D3: Phase II Parity
- [ ] Phase II web UI unchanged
- [ ] All Phase II tests pass
- [ ] API endpoints unchanged
