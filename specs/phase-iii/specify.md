# Phase III Specification — Hackathon II

## Objective
Add an AI-powered conversational interface that allows users to manage their todos
through natural language, while strictly using the existing Phase II backend APIs.

## Core Capabilities
- Natural language todo management
- Intent recognition and mapping to tools
- Tool-based API invocation (MCP)
- Conversational context maintenance
- Action confirmation and feedback

## User Interactions

### Supported Natural Language Commands
| User Says | Intent | Tool Called |
|-----------|--------|-------------|
| "Add a task to buy groceries" | CREATE | `create_todo` |
| "Show my todos" | LIST | `list_todos` |
| "What tasks do I have?" | LIST | `list_todos` |
| "Mark task 3 as done" | UPDATE | `update_todo` |
| "Complete the grocery task" | UPDATE | `update_todo` |
| "Delete task 5" | DELETE | `delete_todo` |
| "Remove the completed tasks" | DELETE | `delete_todo` (multiple) |
| "Show only active tasks" | FILTER | `list_todos` (with filter) |
| "How many tasks do I have?" | COUNT | `list_todos` + count |

### Conversation Examples

**Example 1: Creating a Todo**
```
User: "I need to remember to call the dentist tomorrow"
AI: I'll create a task for you.
    [Tool: create_todo(title="Call the dentist tomorrow")]
AI: Done! I've added "Call the dentist tomorrow" to your tasks.
```

**Example 2: Listing Todos**
```
User: "What's on my list?"
AI: Let me check your tasks.
    [Tool: list_todos()]
AI: You have 3 tasks:
    1. Call the dentist tomorrow (active)
    2. Buy groceries (active)
    3. Review project proposal (completed)
```

**Example 3: Completing a Todo**
```
User: "I finished buying groceries"
AI: I'll mark that as complete.
    [Tool: update_todo(id=2, status="completed")]
AI: Great! "Buy groceries" is now marked as completed.
```

## Functional Requirements

### FR1: Intent Recognition
- Parse natural language to identify action intent
- Extract parameters (title, description, task ID, status)
- Handle ambiguous requests with clarifying questions

### FR2: Tool Invocation
- Map intents to MCP tools
- Pass extracted parameters to tools
- Handle tool responses and errors

### FR3: Response Generation
- Confirm actions taken
- Display results in human-readable format
- Provide helpful suggestions

### FR4: Error Handling
- Handle API errors gracefully
- Explain failures to users
- Suggest alternatives when actions fail

## Non-Functional Requirements

### NFR1: Tool Boundaries
- AI MUST use defined MCP tools only
- AI MUST NOT construct raw HTTP requests
- AI MUST NOT access database directly

### NFR2: Authentication
- AI interface requires user authentication
- JWT token passed through tool invocations
- User sees only their own todos

### NFR3: Transparency
- Show tool invocations in UI (optional toggle)
- Log all AI actions for debugging
- Provide "explain" mode for actions

### NFR4: Performance
- Response time < 3 seconds for simple queries
- Streaming responses for longer operations
- Graceful degradation if AI service unavailable

## Explicit Non-Goals
- Voice interface (text only)
- Multi-language support (English only)
- AI-generated task suggestions
- Automatic task scheduling
- Integration with external calendars
- Offline AI capabilities

## MCP Tool Definitions

### Tool: `create_todo`
```json
{
  "name": "create_todo",
  "description": "Create a new todo task",
  "parameters": {
    "title": { "type": "string", "required": true },
    "description": { "type": "string", "required": false }
  }
}
```

### Tool: `list_todos`
```json
{
  "name": "list_todos",
  "description": "List all todos for the current user",
  "parameters": {
    "status": { "type": "string", "enum": ["all", "active", "completed"] }
  }
}
```

### Tool: `get_todo`
```json
{
  "name": "get_todo",
  "description": "Get details of a specific todo",
  "parameters": {
    "id": { "type": "integer", "required": true }
  }
}
```

### Tool: `update_todo`
```json
{
  "name": "update_todo",
  "description": "Update an existing todo",
  "parameters": {
    "id": { "type": "integer", "required": true },
    "title": { "type": "string", "required": false },
    "description": { "type": "string", "required": false },
    "status": { "type": "string", "enum": ["active", "completed"] }
  }
}
```

### Tool: `delete_todo`
```json
{
  "name": "delete_todo",
  "description": "Delete a todo task",
  "parameters": {
    "id": { "type": "integer", "required": true }
  }
}
```

## UI Components

### Chat Interface
- Message input field
- Message history display
- Tool invocation indicators
- Loading states

### Integration Points
- Embedded in existing Phase II frontend
- Accessible via chat icon/button
- Can be minimized/expanded
- Maintains conversation history per session

## Security Considerations
- AI cannot bypass authentication
- All tool calls go through authenticated API
- No sensitive data in prompts/responses
- Rate limiting on AI requests
