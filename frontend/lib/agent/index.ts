/**
 * Phase III Agent Module
 * [Task]: A3 - Tool contracts frozen, module entry point
 * [Task]: B1, B2, B3 - TodoAgent implementation
 * [Refs]: specs/phase-iii/plan.md#file-structure
 *
 * This module exports all agent-related functionality for Phase III.
 *
 * Structure:
 * - tools.ts: MCP tool definitions (FROZEN)
 * - TodoAgent.ts: Agent logic and system prompt
 */

// Export tool definitions and utilities
export {
  // Tool schemas for OpenAI function calling
  toolSchemas,
  // Tool names constant
  TOOL_NAMES,
  // Type exports
  type ToolName,
  type CreateTodoParams,
  type ListTodosParams,
  type GetTodoParams,
  type UpdateTodoParams,
  type DeleteTodoParams,
  type ToolResult,
  type DeleteResult,
  // Tool implementation class
  TodoTools,
  // Factory function
  createTodoTools,
} from './tools';

// Export TodoAgent and related functionality
export {
  // Agent class
  TodoAgent,
  // System prompt
  SYSTEM_PROMPT,
  // Factory function
  createTodoAgent,
  // Refusal and clarification logic
  REFUSAL_PATTERNS,
  CLARIFICATION_PATTERNS,
  checkForRefusal,
  checkForClarification,
  // Type exports
  type Message,
  type ToolCall,
  type AgentConfig,
  type AgentResponse,
} from './TodoAgent';
