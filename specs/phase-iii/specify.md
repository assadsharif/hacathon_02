# Phase III Specification — AI Todo Chatbot

## Objective
Enable users to interact with the Todo system using natural language,
powered by a controlled AI agent.

## User Capabilities
- Ask about todos
- Create todos via chat
- Update todo status via chat
- Delete todos via chat
- Request summaries

## AI Responsibilities
- Interpret user intent
- Select correct tool
- Validate parameters
- Forward request to backend
- Return backend response verbatim

## AI Limitations
- AI must not make assumptions
- AI must ask for clarification if intent is ambiguous
- AI must refuse unsupported requests

## Tooling Model
- Each backend action = one tool
- Tools mirror Phase II API endpoints
- Tools are the ONLY mutation mechanism

## Non-Goals
- No autonomous AI actions
- No memory beyond conversation
- No AI-generated todos
- No proactive suggestions

## Compatibility Rules
- All behavior must match Phase II API outcomes
- AI responses must reflect backend truth exactly

---

## MCP Tool Definitions

### Tool: `create_todo`
| Property | Value |
|----------|-------|
| Description | Create a new todo task |
| API Endpoint | POST /api/todos |
| Parameters | `title` (required), `description` (optional) |
| Returns | Created todo object |

### Tool: `list_todos`
| Property | Value |
|----------|-------|
| Description | List all todos for the current user |
| API Endpoint | GET /api/todos |
| Parameters | `status` (optional: all, active, completed) |
| Returns | Array of todo objects |

### Tool: `get_todo`
| Property | Value |
|----------|-------|
| Description | Get details of a specific todo |
| API Endpoint | GET /api/todos/{id} |
| Parameters | `id` (required) |
| Returns | Single todo object or 404 error |

### Tool: `update_todo`
| Property | Value |
|----------|-------|
| Description | Update an existing todo |
| API Endpoint | PUT /api/todos/{id} |
| Parameters | `id` (required), `title`, `description`, `status` (optional) |
| Returns | Updated todo object |

### Tool: `delete_todo`
| Property | Value |
|----------|-------|
| Description | Delete a todo task |
| API Endpoint | DELETE /api/todos/{id} |
| Parameters | `id` (required) |
| Returns | Confirmation message |

---

## Conversation Examples

### Creating a Todo
```
User: "Add a task to buy milk"
AI: [Tool: create_todo(title="Buy milk")]
AI: "Created: Buy milk (ID: 5, Status: active)"
```

### Listing Todos
```
User: "What are my tasks?"
AI: [Tool: list_todos()]
AI: "You have 3 tasks:
     1. Buy milk (active)
     2. Call dentist (active)
     3. Review docs (completed)"
```

### Updating a Todo
```
User: "Mark task 1 as done"
AI: [Tool: update_todo(id=1, status="completed")]
AI: "Updated: Buy milk is now completed"
```

### Ambiguous Request
```
User: "Delete it"
AI: "Which task would you like to delete? Please specify the task name or ID."
```

### Unsupported Request
```
User: "Schedule my tasks for next week"
AI: "I can only create, list, update, and delete todos. Scheduling is not supported."
```

---

## Error Handling

| Error | AI Response |
|-------|-------------|
| Todo not found | "Task not found. Use 'list todos' to see available tasks." |
| Invalid status | "Status must be 'active' or 'completed'." |
| Missing title | "Please provide a title for the task." |
| API error | "Something went wrong. Please try again." |
| Auth error | "Please sign in to manage your todos." |
