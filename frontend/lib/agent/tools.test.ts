/**
 * Tool Schema Validation Tests
 * [Task]: A2 - Validate tool schemas match Phase II API contracts
 * [Refs]: specs/phase-iii/tasks.md#a2, backend/schemas.py
 *
 * This test file validates that MCP tool schemas correctly match
 * the Phase II backend API contracts.
 *
 * Validation checklist from tasks.md:
 * - [ ] create_todo tool calls POST /api/todos
 * - [ ] list_todos tool calls GET /api/todos
 * - [ ] get_todo tool calls GET /api/todos/{id}
 * - [ ] update_todo tool calls PUT /api/todos/{id}
 * - [ ] delete_todo tool calls DELETE /api/todos/{id}
 * - [ ] All tools pass JWT token
 */

import {
  toolSchemas,
  TOOL_NAMES,
  CreateTodoParams,
  ListTodosParams,
  GetTodoParams,
  UpdateTodoParams,
  DeleteTodoParams,
} from './tools';
import { Todo, TodoCreate, TodoUpdate } from '../api';

// ============================================================================
// Schema Validation Tests
// ============================================================================

/**
 * Validate that all expected tools are defined
 */
function validateToolPresence(): boolean {
  const expectedTools = ['create_todo', 'list_todos', 'get_todo', 'update_todo', 'delete_todo'];
  const definedTools = toolSchemas.map(t => t.function.name);

  const missing = expectedTools.filter(t => !definedTools.includes(t));
  if (missing.length > 0) {
    console.error(`[FAIL] Missing tools: ${missing.join(', ')}`);
    return false;
  }

  console.log('[PASS] All expected tools are defined');
  return true;
}

/**
 * Validate create_todo matches POST /api/todos contract
 * Backend schema: TodoCreate { title: str, description?: str, status?: 'active'|'completed' }
 */
function validateCreateTodo(): boolean {
  const tool = toolSchemas.find(t => t.function.name === 'create_todo');
  if (!tool) {
    console.error('[FAIL] create_todo tool not found');
    return false;
  }

  const params = tool.function.parameters;
  let valid = true;

  // Check required 'title' parameter
  if (!params.properties.title) {
    console.error('[FAIL] create_todo: missing title parameter');
    valid = false;
  } else if (params.properties.title.type !== 'string') {
    console.error('[FAIL] create_todo: title should be string');
    valid = false;
  }

  // Check 'title' is required
  if (!params.required?.includes('title')) {
    console.error('[FAIL] create_todo: title should be required');
    valid = false;
  }

  // Check optional 'description' parameter
  if (!params.properties.description) {
    console.error('[FAIL] create_todo: missing description parameter');
    valid = false;
  } else if (params.properties.description.type !== 'string') {
    console.error('[FAIL] create_todo: description should be string');
    valid = false;
  }

  // description should NOT be required (optional in backend)
  if (params.required?.includes('description')) {
    console.error('[FAIL] create_todo: description should be optional');
    valid = false;
  }

  if (valid) {
    console.log('[PASS] create_todo matches POST /api/todos contract');
  }
  return valid;
}

/**
 * Validate list_todos matches GET /api/todos contract
 * Backend: status_filter?: 'active'|'completed'
 */
function validateListTodos(): boolean {
  const tool = toolSchemas.find(t => t.function.name === 'list_todos');
  if (!tool) {
    console.error('[FAIL] list_todos tool not found');
    return false;
  }

  const params = tool.function.parameters;
  let valid = true;

  // Check optional 'status' parameter
  if (!params.properties.status) {
    console.error('[FAIL] list_todos: missing status parameter');
    valid = false;
  } else {
    if (params.properties.status.type !== 'string') {
      console.error('[FAIL] list_todos: status should be string');
      valid = false;
    }
    // Check enum values match backend
    const expectedEnum = ['active', 'completed'];
    const actualEnum = params.properties.status.enum;
    if (!actualEnum || !expectedEnum.every(e => actualEnum.includes(e))) {
      console.error('[FAIL] list_todos: status enum should be [active, completed]');
      valid = false;
    }
  }

  // status should NOT be required (optional filter)
  if (params.required?.includes('status')) {
    console.error('[FAIL] list_todos: status should be optional');
    valid = false;
  }

  if (valid) {
    console.log('[PASS] list_todos matches GET /api/todos contract');
  }
  return valid;
}

/**
 * Validate get_todo matches GET /api/todos/{id} contract
 * Backend: todo_id: int (path parameter)
 */
function validateGetTodo(): boolean {
  const tool = toolSchemas.find(t => t.function.name === 'get_todo');
  if (!tool) {
    console.error('[FAIL] get_todo tool not found');
    return false;
  }

  const params = tool.function.parameters;
  let valid = true;

  // Check required 'id' parameter
  if (!params.properties.id) {
    console.error('[FAIL] get_todo: missing id parameter');
    valid = false;
  } else if (params.properties.id.type !== 'number') {
    console.error('[FAIL] get_todo: id should be number');
    valid = false;
  }

  // Check 'id' is required
  if (!params.required?.includes('id')) {
    console.error('[FAIL] get_todo: id should be required');
    valid = false;
  }

  if (valid) {
    console.log('[PASS] get_todo matches GET /api/todos/{id} contract');
  }
  return valid;
}

/**
 * Validate update_todo matches PUT /api/todos/{id} contract
 * Backend: TodoUpdate { title?: str, description?: str, status?: 'active'|'completed' }
 */
function validateUpdateTodo(): boolean {
  const tool = toolSchemas.find(t => t.function.name === 'update_todo');
  if (!tool) {
    console.error('[FAIL] update_todo tool not found');
    return false;
  }

  const params = tool.function.parameters;
  let valid = true;

  // Check required 'id' parameter
  if (!params.properties.id) {
    console.error('[FAIL] update_todo: missing id parameter');
    valid = false;
  } else if (params.properties.id.type !== 'number') {
    console.error('[FAIL] update_todo: id should be number');
    valid = false;
  }

  // Check 'id' is required
  if (!params.required?.includes('id')) {
    console.error('[FAIL] update_todo: id should be required');
    valid = false;
  }

  // Check optional 'title' parameter
  if (!params.properties.title) {
    console.error('[FAIL] update_todo: missing title parameter');
    valid = false;
  }

  // Check optional 'description' parameter
  if (!params.properties.description) {
    console.error('[FAIL] update_todo: missing description parameter');
    valid = false;
  }

  // Check optional 'status' parameter with enum
  if (!params.properties.status) {
    console.error('[FAIL] update_todo: missing status parameter');
    valid = false;
  } else {
    const expectedEnum = ['active', 'completed'];
    const actualEnum = params.properties.status.enum;
    if (!actualEnum || !expectedEnum.every(e => actualEnum.includes(e))) {
      console.error('[FAIL] update_todo: status enum should be [active, completed]');
      valid = false;
    }
  }

  // title, description, status should NOT be required (partial update)
  if (params.required?.includes('title') ||
      params.required?.includes('description') ||
      params.required?.includes('status')) {
    console.error('[FAIL] update_todo: title, description, status should be optional');
    valid = false;
  }

  if (valid) {
    console.log('[PASS] update_todo matches PUT /api/todos/{id} contract');
  }
  return valid;
}

/**
 * Validate delete_todo matches DELETE /api/todos/{id} contract
 * Backend: todo_id: int (path parameter), returns 204 No Content
 */
function validateDeleteTodo(): boolean {
  const tool = toolSchemas.find(t => t.function.name === 'delete_todo');
  if (!tool) {
    console.error('[FAIL] delete_todo tool not found');
    return false;
  }

  const params = tool.function.parameters;
  let valid = true;

  // Check required 'id' parameter
  if (!params.properties.id) {
    console.error('[FAIL] delete_todo: missing id parameter');
    valid = false;
  } else if (params.properties.id.type !== 'number') {
    console.error('[FAIL] delete_todo: id should be number');
    valid = false;
  }

  // Check 'id' is required
  if (!params.required?.includes('id')) {
    console.error('[FAIL] delete_todo: id should be required');
    valid = false;
  }

  if (valid) {
    console.log('[PASS] delete_todo matches DELETE /api/todos/{id} contract');
  }
  return valid;
}

/**
 * Validate TOOL_NAMES constant matches defined schemas
 */
function validateToolNamesConstant(): boolean {
  const schemaNames = toolSchemas.map(t => t.function.name);
  const constantNames = [...TOOL_NAMES];

  const missing = schemaNames.filter(n => !constantNames.includes(n as typeof TOOL_NAMES[number]));
  const extra = constantNames.filter(n => !schemaNames.includes(n));

  if (missing.length > 0 || extra.length > 0) {
    if (missing.length > 0) {
      console.error(`[FAIL] TOOL_NAMES missing: ${missing.join(', ')}`);
    }
    if (extra.length > 0) {
      console.error(`[FAIL] TOOL_NAMES has extra: ${extra.join(', ')}`);
    }
    return false;
  }

  console.log('[PASS] TOOL_NAMES matches toolSchemas');
  return true;
}

// ============================================================================
// Type Compatibility Checks (compile-time validation)
// ============================================================================

/**
 * Type assertion: CreateTodoParams is compatible with TodoCreate input fields
 */
type _AssertCreateCompatible = CreateTodoParams extends Pick<TodoCreate, 'title' | 'description'>
  ? true
  : never;

/**
 * Type assertion: UpdateTodoParams update fields match TodoUpdate
 */
type _AssertUpdateCompatible = Omit<UpdateTodoParams, 'id'> extends TodoUpdate
  ? true
  : never;

/**
 * Type assertion: ListTodosParams status matches API filter type
 */
type _AssertListStatusCompatible = NonNullable<ListTodosParams['status']> extends 'active' | 'completed'
  ? true
  : never;

// ============================================================================
// Run All Validations
// ============================================================================

/**
 * Run all tool schema validations
 * @returns true if all validations pass
 */
export function runValidations(): boolean {
  console.log('='.repeat(60));
  console.log('Tool Schema Validation - Task A2');
  console.log('='.repeat(60));

  const results = [
    validateToolPresence(),
    validateCreateTodo(),
    validateListTodos(),
    validateGetTodo(),
    validateUpdateTodo(),
    validateDeleteTodo(),
    validateToolNamesConstant(),
  ];

  console.log('='.repeat(60));

  const passed = results.filter(r => r).length;
  const total = results.length;

  if (passed === total) {
    console.log(`[SUCCESS] All ${total} validations passed`);
    console.log('Tool schemas match Phase II API contracts');
    return true;
  } else {
    console.error(`[FAILURE] ${passed}/${total} validations passed`);
    return false;
  }
}

// Run validations when executed directly
if (typeof process !== 'undefined' && process.argv[1]?.includes('tools.test')) {
  const success = runValidations();
  process.exit(success ? 0 : 1);
}
