/**
 * TodoAgent - AI Conversational Interface for Todo Management
 * [Task]: B1 - Define TodoAgent with system prompt and role
 * [Task]: B2 - Bind MCP tools to agent
 * [Task]: B3 - Implement refusal and clarification logic
 * [Refs]: specs/phase-iii/specify.md, specs/phase-iii/plan.md#agent-design
 *
 * Core Principles (from specify.md):
 * - AI is an INTERFACE, not a decision-maker
 * - All actions must go through tools (tool-first execution)
 * - AI must not make assumptions
 * - AI must ask for clarification if intent is ambiguous
 * - AI must refuse unsupported requests
 *
 * Non-Goals (from specify.md):
 * - No autonomous AI actions
 * - No memory beyond conversation
 * - No AI-generated todos
 * - No proactive suggestions
 */

import { toolSchemas, TodoTools, createTodoTools, TOOL_NAMES, ToolResult } from './tools';
import { Todo } from '../api';

// ============================================================================
// System Prompt
// [Task]: B1 - Define TodoAgent role and scope
// ============================================================================

/**
 * System prompt for the TodoAgent.
 * Defines the agent's role, capabilities, and behavioral constraints.
 * [Refs]: specify.md#ai-responsibilities, specify.md#ai-limitations
 */
export const SYSTEM_PROMPT = `You are a Todo Management Assistant. Your role is to help users manage their todo list through natural language.

## Your Capabilities
You can ONLY perform these actions using the provided tools:
- Create new todos (create_todo)
- List todos with optional filtering (list_todos)
- Get details of a specific todo (get_todo)
- Update existing todos (update_todo)
- Delete todos (delete_todo)

## Rules You MUST Follow

### Tool-First Execution
1. ALWAYS use tools to interact with the todo system. Never invent or assume data.
2. When the user asks to see, create, update, or delete todos, use the appropriate tool.
3. Report tool results exactly as received - do not modify or embellish the data.

### Clarification Requirements
Ask for clarification when:
- The user says "delete it" or "mark it done" without specifying which todo
- The user's request is vague about which todo they're referring to
- You need a todo ID but the user only gave a description

### Refusal Requirements
Politely refuse and explain when the user asks for:
- Scheduling or calendar integration ("Schedule my tasks for next week")
- Reminders or notifications ("Remind me about this")
- AI-generated task suggestions ("What should I work on?")
- Anything outside CRUD operations on todos

### Response Format
- After creating a todo: Confirm with the title and new ID
- After listing todos: Present as a numbered list with status
- After updating: Confirm what was changed
- After deleting: Confirm the deletion
- On errors: Provide the error message and suggest alternatives

## Examples of Proper Responses

User: "Add a task to buy milk"
→ Use create_todo with title="Buy milk"
→ Respond: "Created: 'Buy milk' (ID: 5, Status: active)"

User: "What are my tasks?"
→ Use list_todos
→ Respond with numbered list

User: "Mark task 1 as done"
→ Use update_todo with id=1, status="completed"
→ Respond: "Updated: 'Buy milk' is now completed"

User: "Delete it"
→ Ask: "Which task would you like to delete? Please specify the task name or ID."

User: "Schedule my tasks"
→ Refuse: "I can only create, list, update, and delete todos. Scheduling is not supported."`;

// ============================================================================
// Types
// ============================================================================

/**
 * Message in the conversation
 */
export interface Message {
  role: 'system' | 'user' | 'assistant' | 'tool';
  content: string;
  tool_call_id?: string;
  tool_calls?: ToolCall[];
}

/**
 * Tool call from the assistant
 */
export interface ToolCall {
  id: string;
  type: 'function';
  function: {
    name: string;
    arguments: string;
  };
}

/**
 * Agent configuration
 */
export interface AgentConfig {
  /** JWT token for API authentication */
  token: string;
  /** Optional custom system prompt */
  systemPrompt?: string;
  /** Callback for when tools are called */
  onToolCall?: (toolName: string, args: unknown, result: ToolResult<unknown>) => void;
}

/**
 * Agent response
 */
export interface AgentResponse {
  /** Text response to the user */
  message: string;
  /** Tools that were called during this turn */
  toolCalls: Array<{
    name: string;
    args: unknown;
    result: ToolResult<unknown>;
  }>;
}

// ============================================================================
// TodoAgent Class
// [Task]: B1, B2, B3 - Agent implementation
// ============================================================================

/**
 * TodoAgent - Conversational interface for todo management.
 *
 * This agent:
 * - Interprets user intent and selects appropriate tools
 * - Executes tools against the Phase II API
 * - Formats responses for the user
 * - Implements refusal for unsupported requests
 * - Asks for clarification on ambiguous requests
 *
 * [Refs]: specs/phase-iii/plan.md#data-flow
 */
export class TodoAgent {
  private tools: TodoTools;
  private config: AgentConfig;
  private conversationHistory: Message[];

  /**
   * Create a new TodoAgent instance.
   * [Task]: B1 - Agent initialization with system prompt
   *
   * @param config - Agent configuration including JWT token
   */
  constructor(config: AgentConfig) {
    this.config = config;
    this.tools = createTodoTools(config.token);
    this.conversationHistory = [
      {
        role: 'system',
        content: config.systemPrompt || SYSTEM_PROMPT,
      },
    ];
  }

  /**
   * Get the tool schemas for OpenAI function calling.
   * [Task]: B2 - Bind MCP tools to agent
   */
  getToolSchemas() {
    return toolSchemas;
  }

  /**
   * Get the current conversation history.
   */
  getConversationHistory(): Message[] {
    return [...this.conversationHistory];
  }

  /**
   * Clear conversation history (keeps system prompt).
   */
  clearHistory(): void {
    this.conversationHistory = [this.conversationHistory[0]];
  }

  /**
   * Execute a tool call and return the result.
   * [Task]: B2 - Tool execution
   *
   * @param toolCall - The tool call from the assistant
   * @returns Tool result
   */
  async executeTool(toolCall: ToolCall): Promise<ToolResult<unknown>> {
    const { name, arguments: argsJson } = toolCall.function;

    // Parse arguments
    let args: Record<string, unknown>;
    try {
      args = JSON.parse(argsJson);
    } catch {
      return {
        success: false,
        error: `Invalid JSON in tool arguments: ${argsJson}`,
      };
    }

    // Execute the tool
    const result = await this.tools.executeTool(name, args);

    // Call the callback if provided
    if (this.config.onToolCall) {
      this.config.onToolCall(name, args, result);
    }

    return result;
  }

  /**
   * Add a user message to the conversation.
   *
   * @param content - User's message
   */
  addUserMessage(content: string): void {
    this.conversationHistory.push({
      role: 'user',
      content,
    });
  }

  /**
   * Add an assistant message to the conversation.
   *
   * @param content - Assistant's response
   * @param toolCalls - Optional tool calls made by the assistant
   */
  addAssistantMessage(content: string, toolCalls?: ToolCall[]): void {
    this.conversationHistory.push({
      role: 'assistant',
      content,
      tool_calls: toolCalls,
    });
  }

  /**
   * Add a tool result to the conversation.
   *
   * @param toolCallId - ID of the tool call
   * @param result - Result from the tool
   */
  addToolResult(toolCallId: string, result: ToolResult<unknown>): void {
    this.conversationHistory.push({
      role: 'tool',
      tool_call_id: toolCallId,
      content: JSON.stringify(result),
    });
  }

  /**
   * Format a todo for display.
   * [Task]: B1 - Response formatting
   */
  formatTodo(todo: Todo): string {
    return `${todo.title} (ID: ${todo.id}, Status: ${todo.status})`;
  }

  /**
   * Format a list of todos for display.
   * [Task]: B1 - Response formatting
   */
  formatTodoList(todos: Todo[]): string {
    if (todos.length === 0) {
      return 'You have no todos.';
    }

    const lines = todos.map((todo, index) =>
      `${index + 1}. ${todo.title} (${todo.status})${todo.description ? ` - ${todo.description}` : ''}`
    );

    return `You have ${todos.length} todo${todos.length === 1 ? '' : 's'}:\n${lines.join('\n')}`;
  }

  /**
   * Format a tool result for user display.
   * [Task]: B1 - Response formatting based on specify.md examples
   *
   * @param toolName - Name of the tool that was called
   * @param result - Result from the tool
   * @returns Formatted string for user display
   */
  formatToolResult(toolName: string, result: ToolResult<unknown>): string {
    if (!result.success) {
      // Error handling from specify.md
      if (result.error?.includes('not found')) {
        return "Task not found. Use 'list todos' to see available tasks.";
      }
      if (result.error?.includes('Authentication')) {
        return 'Please sign in to manage your todos.';
      }
      return result.error || 'Something went wrong. Please try again.';
    }

    switch (toolName) {
      case 'create_todo': {
        const todo = result.data as Todo;
        return `Created: '${todo.title}' (ID: ${todo.id}, Status: ${todo.status})`;
      }

      case 'list_todos': {
        const todos = result.data as Todo[];
        return this.formatTodoList(todos);
      }

      case 'get_todo': {
        const todo = result.data as Todo;
        let response = `Todo #${todo.id}: ${todo.title}\n`;
        response += `Status: ${todo.status}\n`;
        if (todo.description) {
          response += `Description: ${todo.description}\n`;
        }
        response += `Created: ${new Date(todo.created_at).toLocaleDateString()}`;
        return response;
      }

      case 'update_todo': {
        const todo = result.data as Todo;
        return `Updated: '${todo.title}' is now ${todo.status}`;
      }

      case 'delete_todo': {
        const deleteResult = result.data as { message: string; deleted_id: number };
        return `Deleted todo #${deleteResult.deleted_id}`;
      }

      default:
        return JSON.stringify(result.data);
    }
  }
}

// ============================================================================
// Refusal and Clarification Patterns
// [Task]: B3 - Define refusal and clarification logic
// ============================================================================

/**
 * Patterns that should trigger a refusal response.
 * [Refs]: specify.md#unsupported-request, tasks.md#b3
 */
export const REFUSAL_PATTERNS = [
  { pattern: /schedul/i, response: 'I can only create, list, update, and delete todos. Scheduling is not supported.' },
  { pattern: /remind/i, response: 'I can only create, list, update, and delete todos. Reminders are not supported.' },
  { pattern: /notif/i, response: 'I can only create, list, update, and delete todos. Notifications are not supported.' },
  { pattern: /suggest|recommend|what should i/i, response: 'I can only manage your existing todos. I cannot suggest or recommend tasks.' },
  { pattern: /calendar/i, response: 'I can only create, list, update, and delete todos. Calendar integration is not supported.' },
  { pattern: /priority|prioritize/i, response: 'I can only manage todo status (active/completed). Priority levels are not supported.' },
  { pattern: /due date|deadline/i, response: 'I can only manage todo status (active/completed). Due dates are not supported.' },
];

/**
 * Patterns that should trigger a clarification request.
 * [Refs]: specify.md#ambiguous-request, tasks.md#b3
 */
export const CLARIFICATION_PATTERNS = [
  { pattern: /delete it|remove it/i, response: 'Which task would you like to delete? Please specify the task name or ID.' },
  { pattern: /mark it|complete it|finish it/i, response: 'Which task would you like to mark as completed? Please specify the task name or ID.' },
  { pattern: /update it|change it|edit it/i, response: 'Which task would you like to update? Please specify the task name or ID.' },
  { pattern: /^it$/i, response: 'Could you please specify which task you\'re referring to?' },
];

/**
 * Check if a message should trigger a refusal.
 * [Task]: B3 - Refusal logic
 *
 * @param message - User message to check
 * @returns Refusal response or null if no refusal needed
 */
export function checkForRefusal(message: string): string | null {
  for (const { pattern, response } of REFUSAL_PATTERNS) {
    if (pattern.test(message)) {
      return response;
    }
  }
  return null;
}

/**
 * Check if a message should trigger a clarification request.
 * [Task]: B3 - Clarification logic
 *
 * @param message - User message to check
 * @returns Clarification response or null if no clarification needed
 */
export function checkForClarification(message: string): string | null {
  for (const { pattern, response } of CLARIFICATION_PATTERNS) {
    if (pattern.test(message)) {
      return response;
    }
  }
  return null;
}

// ============================================================================
// Factory Function
// ============================================================================

/**
 * Create a new TodoAgent instance.
 * [Task]: B1 - Agent factory
 *
 * @param token - JWT token for API authentication
 * @param options - Optional configuration
 * @returns Configured TodoAgent instance
 *
 * @example
 * ```typescript
 * const agent = createTodoAgent(session.accessToken);
 * agent.addUserMessage("Create a task to buy milk");
 * // Process with OpenAI API, execute tools, format response
 * ```
 */
export function createTodoAgent(
  token: string,
  options?: Partial<Omit<AgentConfig, 'token'>>
): TodoAgent {
  return new TodoAgent({
    token,
    ...options,
  });
}
