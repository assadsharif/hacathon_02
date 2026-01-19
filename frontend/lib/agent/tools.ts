/**
 * MCP Tool Definitions for Phase III AI Integration
 * [Task]: A1 - Define MCP tools for each API endpoint
 * [Task]: A3 - Tool contracts frozen as of 2026-01-19
 * [Refs]: specs/phase-iii/plan.md#tool-contracts, specs/phase-iii/tasks.md#a1
 *
 * ============================================================================
 * FROZEN CONTRACT - DO NOT MODIFY TOOL SIGNATURES
 * ============================================================================
 * These tool contracts were validated against Phase II API (Task A2) and
 * frozen (Task A3). Any changes require spec amendment and re-validation.
 *
 * Frozen date: 2026-01-19
 * Validated by: tools.test.ts (7/7 checks passed)
 * ============================================================================
 *
 * This module defines MCP-compatible tools that wrap Phase II API endpoints.
 * Each tool:
 * - Maps to a single Phase II API endpoint
 * - Passes JWT token for authentication
 * - Returns structured responses for the TodoAgent
 *
 * Tool Contracts (from plan.md):
 * | Tool          | Input                                    | Output          |
 * |---------------|------------------------------------------|-----------------|
 * | create_todo   | title, description?                      | Todo object     |
 * | list_todos    | status?                                  | Todo[]          |
 * | get_todo      | id                                       | Todo            |
 * | update_todo   | id, title?, description?, status?        | Todo            |
 * | delete_todo   | id                                       | Success message |
 */

import { TodoApi, Todo, TodoCreate, TodoUpdate } from '../api';

// ============================================================================
// Tool Parameter Types
// [Task]: A1 - Type definitions matching plan.md tool contracts
// ============================================================================

/**
 * Parameters for create_todo tool
 * [Refs]: plan.md#tool-contracts - create_todo: title, description? -> Todo
 */
export interface CreateTodoParams {
  /** Todo title (required, 1-200 characters) */
  title: string;
  /** Optional description */
  description?: string;
}

/**
 * Parameters for list_todos tool
 * [Refs]: plan.md#tool-contracts - list_todos: status? -> Todo[]
 */
export interface ListTodosParams {
  /** Optional filter by status */
  status?: 'active' | 'completed';
}

/**
 * Parameters for get_todo tool
 * [Refs]: plan.md#tool-contracts - get_todo: id -> Todo
 */
export interface GetTodoParams {
  /** Todo ID (required) */
  id: number;
}

/**
 * Parameters for update_todo tool
 * [Refs]: plan.md#tool-contracts - update_todo: id, title?, description?, status? -> Todo
 */
export interface UpdateTodoParams {
  /** Todo ID (required) */
  id: number;
  /** Updated title */
  title?: string;
  /** Updated description */
  description?: string;
  /** Updated status */
  status?: 'active' | 'completed';
}

/**
 * Parameters for delete_todo tool
 * [Refs]: plan.md#tool-contracts - delete_todo: id -> Success message
 */
export interface DeleteTodoParams {
  /** Todo ID (required) */
  id: number;
}

// ============================================================================
// Tool Result Types
// [Task]: A1 - Structured responses for agent consumption
// ============================================================================

/**
 * Standard tool result wrapper
 */
export interface ToolResult<T> {
  success: boolean;
  data?: T;
  error?: string;
}

/**
 * Delete operation result
 */
export interface DeleteResult {
  message: string;
  deleted_id: number;
}

// ============================================================================
// Tool Schema Definitions (OpenAI Function Calling Format)
// [Task]: A1 - MCP-compatible tool schemas for OpenAI Agents SDK
// ============================================================================

/**
 * Tool schema definitions for OpenAI function calling.
 * These schemas describe the tools available to the TodoAgent.
 * [Refs]: specs/phase-iii/tasks.md#a1 - All tools pass JWT token
 */
export const toolSchemas = [
  {
    type: 'function' as const,
    function: {
      name: 'create_todo',
      description: 'Create a new todo item. Use this when the user wants to add a new task.',
      parameters: {
        type: 'object',
        properties: {
          title: {
            type: 'string',
            description: 'The title of the todo (1-200 characters)',
            minLength: 1,
            maxLength: 200,
          },
          description: {
            type: 'string',
            description: 'Optional description for the todo',
          },
        },
        required: ['title'],
        additionalProperties: false,
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'list_todos',
      description: 'List all todos for the current user. Can optionally filter by status (active or completed).',
      parameters: {
        type: 'object',
        properties: {
          status: {
            type: 'string',
            enum: ['active', 'completed'],
            description: 'Filter todos by status. Omit to get all todos.',
          },
        },
        additionalProperties: false,
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'get_todo',
      description: 'Get a specific todo by its ID. Use this to retrieve details of a single todo.',
      parameters: {
        type: 'object',
        properties: {
          id: {
            type: 'number',
            description: 'The unique identifier of the todo',
          },
        },
        required: ['id'],
        additionalProperties: false,
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'update_todo',
      description: 'Update an existing todo. Can update title, description, and/or status. Use this to mark todos as completed or modify their content.',
      parameters: {
        type: 'object',
        properties: {
          id: {
            type: 'number',
            description: 'The unique identifier of the todo to update',
          },
          title: {
            type: 'string',
            description: 'New title for the todo (1-200 characters)',
            minLength: 1,
            maxLength: 200,
          },
          description: {
            type: 'string',
            description: 'New description for the todo',
          },
          status: {
            type: 'string',
            enum: ['active', 'completed'],
            description: 'New status for the todo',
          },
        },
        required: ['id'],
        additionalProperties: false,
      },
    },
  },
  {
    type: 'function' as const,
    function: {
      name: 'delete_todo',
      description: 'Delete a todo by its ID. This action cannot be undone.',
      parameters: {
        type: 'object',
        properties: {
          id: {
            type: 'number',
            description: 'The unique identifier of the todo to delete',
          },
        },
        required: ['id'],
        additionalProperties: false,
      },
    },
  },
] as const;

// ============================================================================
// Tool Implementations
// [Task]: A1 - Tool functions wrapping Phase II API with JWT auth
// ============================================================================

/**
 * MCP Tools class that wraps Phase II API endpoints.
 * All operations require a valid JWT token for authentication.
 * [Refs]: specs/phase-iii/tasks.md#a1 - All tools pass JWT token
 */
export class TodoTools {
  private api: TodoApi;

  /**
   * Create a new TodoTools instance.
   * @param token - JWT token for authenticated API calls
   */
  constructor(token: string) {
    this.api = new TodoApi(undefined, token);
  }

  /**
   * Create a new todo.
   * [Tool]: create_todo
   * [API]: POST /api/todos
   * [Refs]: plan.md#tool-contracts - create_todo: title, description? -> Todo
   *
   * @param params - Create parameters (title required, description optional)
   * @returns ToolResult containing the created Todo or error
   */
  async createTodo(params: CreateTodoParams): Promise<ToolResult<Todo>> {
    try {
      const payload: TodoCreate = {
        title: params.title,
        description: params.description ?? null,
        status: 'active', // New todos are always active
      };

      const todo = await this.api.createTodo(payload);

      return {
        success: true,
        data: todo,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to create todo',
      };
    }
  }

  /**
   * List all todos with optional status filter.
   * [Tool]: list_todos
   * [API]: GET /api/todos
   * [Refs]: plan.md#tool-contracts - list_todos: status? -> Todo[]
   *
   * @param params - Optional status filter
   * @returns ToolResult containing array of Todos or error
   */
  async listTodos(params: ListTodosParams = {}): Promise<ToolResult<Todo[]>> {
    try {
      const todos = await this.api.listTodos(params.status);

      return {
        success: true,
        data: todos,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to list todos',
      };
    }
  }

  /**
   * Get a single todo by ID.
   * [Tool]: get_todo
   * [API]: GET /api/todos/{id}
   * [Refs]: plan.md#tool-contracts - get_todo: id -> Todo
   *
   * @param params - Todo ID
   * @returns ToolResult containing the Todo or error
   */
  async getTodo(params: GetTodoParams): Promise<ToolResult<Todo>> {
    try {
      const todo = await this.api.getTodo(params.id);

      return {
        success: true,
        data: todo,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : `Failed to get todo ${params.id}`,
      };
    }
  }

  /**
   * Update an existing todo.
   * [Tool]: update_todo
   * [API]: PUT /api/todos/{id}
   * [Refs]: plan.md#tool-contracts - update_todo: id, title?, description?, status? -> Todo
   *
   * @param params - Todo ID and fields to update
   * @returns ToolResult containing the updated Todo or error
   */
  async updateTodo(params: UpdateTodoParams): Promise<ToolResult<Todo>> {
    try {
      const { id, ...updateFields } = params;

      // Only include fields that were actually provided
      const payload: TodoUpdate = {};
      if (updateFields.title !== undefined) payload.title = updateFields.title;
      if (updateFields.description !== undefined) payload.description = updateFields.description;
      if (updateFields.status !== undefined) payload.status = updateFields.status;

      const todo = await this.api.updateTodo(id, payload);

      return {
        success: true,
        data: todo,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : `Failed to update todo ${params.id}`,
      };
    }
  }

  /**
   * Delete a todo by ID.
   * [Tool]: delete_todo
   * [API]: DELETE /api/todos/{id}
   * [Refs]: plan.md#tool-contracts - delete_todo: id -> Success message
   *
   * @param params - Todo ID to delete
   * @returns ToolResult containing success message or error
   */
  async deleteTodo(params: DeleteTodoParams): Promise<ToolResult<DeleteResult>> {
    try {
      await this.api.deleteTodo(params.id);

      return {
        success: true,
        data: {
          message: `Todo ${params.id} deleted successfully`,
          deleted_id: params.id,
        },
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : `Failed to delete todo ${params.id}`,
      };
    }
  }

  /**
   * Execute a tool by name with given arguments.
   * This method dispatches to the appropriate tool implementation.
   * [Task]: A1 - Tool execution dispatcher for agent integration
   *
   * @param toolName - Name of the tool to execute
   * @param args - Tool arguments (parsed from JSON)
   * @returns ToolResult from the executed tool
   */
  async executeTool(
    toolName: string,
    args: Record<string, unknown>
  ): Promise<ToolResult<unknown>> {
    switch (toolName) {
      case 'create_todo':
        return this.createTodo(args as unknown as CreateTodoParams);

      case 'list_todos':
        return this.listTodos(args as unknown as ListTodosParams);

      case 'get_todo':
        return this.getTodo(args as unknown as GetTodoParams);

      case 'update_todo':
        return this.updateTodo(args as unknown as UpdateTodoParams);

      case 'delete_todo':
        return this.deleteTodo(args as unknown as DeleteTodoParams);

      default:
        return {
          success: false,
          error: `Unknown tool: ${toolName}. Available tools: create_todo, list_todos, get_todo, update_todo, delete_todo`,
        };
    }
  }
}

/**
 * Create a TodoTools instance with the given JWT token.
 * [Refs]: specs/phase-iii/tasks.md#a1 - All tools pass JWT token
 *
 * @param token - JWT token from authenticated session
 * @returns TodoTools instance ready for tool execution
 *
 * @example
 * ```typescript
 * const tools = createTodoTools(session.accessToken);
 * const result = await tools.createTodo({ title: 'New task' });
 * ```
 */
export function createTodoTools(token: string): TodoTools {
  return new TodoTools(token);
}

// Export tool names for validation
export const TOOL_NAMES = ['create_todo', 'list_todos', 'get_todo', 'update_todo', 'delete_todo'] as const;
export type ToolName = typeof TOOL_NAMES[number];
