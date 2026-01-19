# Phase III Tasks — Hackathon II

## Task Group A: MCP Server

A1. Create MCP server project structure
   - Initialize Node.js/TypeScript project
   - Install @modelcontextprotocol/sdk
   - Configure TypeScript and build setup
   - Create basic server entry point

A2. Implement `create_todo` tool
   - Define tool schema
   - Implement handler that calls POST /api/todos
   - Pass JWT token from context
   - Return formatted response

A3. Implement `list_todos` tool
   - Define tool schema with optional status filter
   - Implement handler that calls GET /api/todos
   - Format response for AI consumption

A4. Implement `get_todo` tool
   - Define tool schema
   - Implement handler that calls GET /api/todos/{id}
   - Handle not found errors

A5. Implement `update_todo` tool
   - Define tool schema with optional fields
   - Implement handler that calls PUT /api/todos/{id}
   - Support partial updates

A6. Implement `delete_todo` tool
   - Define tool schema
   - Implement handler that calls DELETE /api/todos/{id}
   - Return confirmation message

A7. Test MCP tools independently
   - Write test script for each tool
   - Verify API calls are correct
   - Verify authentication passthrough

## Task Group B: Agent Configuration

B1. Set up OpenAI Agents SDK
   - Install openai package
   - Configure API key
   - Create agent configuration file

B2. Define system prompt
   - Write clear instructions for todo management
   - Define response format guidelines
   - Specify tool usage rules
   - Include examples

B3. Register MCP tools with agent
   - Connect MCP server to agent
   - Map tool definitions
   - Configure tool permissions

B4. Implement conversation context
   - Store conversation history
   - Pass user context (auth token)
   - Handle context window limits

## Task Group C: ChatKit UI

C1. Add chat route to frontend
   - Create /chat page
   - Add navigation link
   - Protect route (require auth)

C2. Implement ChatWindow component
   - Message display area
   - Input field with send button
   - Scrolling behavior

C3. Implement MessageList component
   - User messages (right aligned)
   - AI messages (left aligned)
   - Tool invocation display (collapsible)
   - Loading indicator

C4. Connect ChatKit to Agent
   - WebSocket or streaming connection
   - Send user messages
   - Receive AI responses
   - Handle tool invocations

C5. Add tool visibility toggle
   - Setting to show/hide tool calls
   - Store preference in localStorage
   - Update UI based on setting

## Task Group D: Integration & Testing

D1. End-to-end conversation testing
   - Test create flow: "Add task X"
   - Test list flow: "Show my tasks"
   - Test update flow: "Complete task Y"
   - Test delete flow: "Remove task Z"

D2. Error handling verification
   - Test invalid requests
   - Test API failures
   - Test authentication errors
   - Verify error messages are helpful

D3. Phase II regression testing
   - Run existing Phase II tests
   - Verify web UI still works
   - Verify API endpoints unchanged

D4. Phase I regression testing
   - Run Phase I tests
   - Verify CLI still works

## Task Group E: Documentation

E1. Update README
   - Add Phase III section
   - Document AI chat feature
   - Include conversation examples

E2. Create user guide
   - How to use chat interface
   - Supported commands
   - Tips and limitations

E3. Create developer guide
   - MCP server architecture
   - Adding new tools
   - Debugging AI interactions

## Task Discipline
- One task at a time
- Specs referenced in every task
- No task expands scope
- AI MUST use tools (no direct API calls)
- Phase I & II remain unchanged
