# Phase III Plan — Hackathon II

## Strategy
Add AI conversational layer on top of Phase II without modifying existing systems.
AI acts as a translation layer: Natural Language → Tools → Backend API → Response.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE III: AI LAYER (NEW)                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 OpenAI ChatKit UI                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │   │
│  │  │  Chat Input  │  │  Message     │  │  Tool Display   │   │   │
│  │  │  Field       │  │  History     │  │  (optional)     │   │   │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘   │   │
│  └──────────────────────────┬──────────────────────────────────┘   │
│                             │                                       │
│  ┌──────────────────────────▼──────────────────────────────────┐   │
│  │              OpenAI Agents SDK                               │   │
│  │  ┌─────────────────────────────────────────────────────┐    │   │
│  │  │  Agent: "Todo Assistant"                             │    │   │
│  │  │  - System Prompt: Todo management rules             │    │   │
│  │  │  - Available Tools: MCP tools                       │    │   │
│  │  │  - Context: User session + conversation history     │    │   │
│  │  └─────────────────────────────────────────────────────┘    │   │
│  └──────────────────────────┬──────────────────────────────────┘   │
│                             │                                       │
│  ┌──────────────────────────▼──────────────────────────────────┐   │
│  │                    MCP Server                                │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐  │   │
│  │  │create_todo │ │list_todos  │ │update_todo │ │delete_   │  │   │
│  │  │            │ │            │ │            │ │todo      │  │   │
│  │  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └────┬─────┘  │   │
│  └────────┼──────────────┼──────────────┼─────────────┼────────┘   │
│           │              │              │             │             │
└───────────┼──────────────┼──────────────┼─────────────┼─────────────┘
            │              │              │             │
            ▼              ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 PHASE II: BACKEND (UNCHANGED)                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Endpoints                         │   │
│  │  POST /api/todos  GET /api/todos  PUT /api/todos/{id}  ...  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    PostgreSQL (Neon)                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Milestones

### M1: MCP Server Setup
- Create MCP server with tool definitions
- Implement tool handlers that call Phase II APIs
- Pass authentication tokens through tools
- Test tools independently

### M2: Agent Configuration
- Configure OpenAI Agent with system prompt
- Define tool bindings
- Set up conversation context management
- Implement response formatting

### M3: ChatKit UI Integration
- Add chat interface to Phase II frontend
- Connect ChatKit to Agent
- Display messages and tool invocations
- Handle loading and error states

### M4: End-to-End Testing
- Test full conversation flows
- Validate tool invocations
- Verify authentication passthrough
- Confirm Phase II unchanged

### M5: Polish & Documentation
- Add tool invocation visibility toggle
- Improve error messages
- Document conversation examples
- Create user guide

## Technical Decisions

### Why MCP (Model Context Protocol)?
- Standard interface for AI tool invocation
- Clear separation between AI and backend
- Traceable and auditable actions
- Works with multiple AI providers

### Why OpenAI Agents SDK?
- Production-ready agent orchestration
- Built-in conversation management
- Tool calling support
- Streaming responses

### Why ChatKit?
- Pre-built chat UI components
- Integrates with OpenAI ecosystem
- Customizable appearance
- Handles message threading

## Risk Controls
- All tool calls logged
- AI cannot exceed tool permissions
- Rate limiting on AI requests
- Fallback to manual UI if AI fails

## Completion Criteria
- [ ] User can create todo via natural language
- [ ] User can list todos via natural language
- [ ] User can update todos via natural language
- [ ] User can delete todos via natural language
- [ ] All actions go through Phase II APIs
- [ ] Phase II tests still pass
- [ ] Phase I tests still pass
- [ ] Tool invocations are visible (optional toggle)

## Environment Variables (New)

```bash
# Phase III - AI Configuration
OPENAI_API_KEY=sk-...
MCP_SERVER_URL=http://localhost:3001
AI_MODEL=gpt-4o-mini
AI_MAX_TOKENS=1000
```

## File Structure (New)

```
frontend/
├── app/
│   └── chat/              # New chat page
│       └── page.tsx
├── components/
│   └── ai/                # AI components
│       ├── ChatWindow.tsx
│       ├── MessageList.tsx
│       ├── ToolDisplay.tsx
│       └── ChatInput.tsx
└── lib/
    └── mcp/               # MCP client
        ├── client.ts
        └── tools.ts

mcp-server/                # New MCP server
├── server.ts
├── tools/
│   ├── create_todo.ts
│   ├── list_todos.ts
│   ├── update_todo.ts
│   ├── delete_todo.ts
│   └── get_todo.ts
├── package.json
└── tsconfig.json
```
