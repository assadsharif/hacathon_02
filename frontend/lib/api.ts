/**
 * API Client for Phase II Backend
 * [Task]: AUTH-C5 - Updated to include JWT authentication
 *
 * This module provides type-safe API communication with the FastAPI backend.
 * All API calls include JWT tokens in the Authorization header for authentication.
 */

// API Base URL - uses Next.js API rewrites in development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Todo type matching backend schema (Phase I + Phase II)
 * [Task]: AUTH-C5 - Added user_id for user-scoped data
 */
export interface Todo {
  id: number;
  user_id: string | null;  // UUID of the todo owner
  title: string;
  description: string | null;
  status: 'active' | 'completed';
  created_at: string;
  updated_at: string;
}

/**
 * Todo creation payload
 */
export interface TodoCreate {
  title: string;
  description?: string | null;
  status?: 'active' | 'completed';
}

/**
 * Todo update payload (partial)
 */
export interface TodoUpdate {
  title?: string;
  description?: string | null;
  status?: 'active' | 'completed';
}

/**
 * API error response
 */
export interface ApiError {
  detail: string;
}

/**
 * API Client class for Todo operations
 * [Task]: AUTH-C5 - Updated to support JWT authentication
 */
export class TodoApi {
  private baseUrl: string;
  private token: string | null;

  constructor(baseUrl: string = API_BASE_URL, token: string | null = null) {
    this.baseUrl = baseUrl;
    this.token = token;
  }

  /**
   * Set the JWT token for authenticated requests.
   * [Task]: AUTH-C5 - JWT token management
   *
   * @param token - JWT token from Better Auth session
   *
   * Example:
   *   const api = new TodoApi();
   *   api.setToken(session.token);
   */
  setToken(token: string | null) {
    this.token = token;
  }

  /**
   * Get authorization headers for authenticated requests.
   * [Task]: AUTH-C5 - Attach JWT to all requests
   *
   * @returns Headers object with Authorization header if token exists
   */
  private getAuthHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  /**
   * Handle API response and errors
   * [Task]: AUTH-C5 - Enhanced error handling for 401 Unauthorized
   */
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        detail: `HTTP ${response.status}: ${response.statusText}`,
      }));

      // Special handling for authentication errors
      if (response.status === 401) {
        throw new Error('Authentication required. Please sign in.');
      }

      throw new Error(error.detail);
    }

    // Handle 204 No Content (DELETE responses)
    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  }

  /**
   * List all todos with optional status filter
   * [Task]: AUTH-C5 - Now includes JWT token in Authorization header
   */
  async listTodos(statusFilter?: 'active' | 'completed'): Promise<Todo[]> {
    const url = new URL(`${this.baseUrl}/api/todos`);
    if (statusFilter) {
      url.searchParams.set('status_filter', statusFilter);
    }

    const response = await fetch(url.toString(), {
      cache: 'no-store', // Disable caching for dynamic data
      headers: this.getAuthHeaders(),
    });

    const data = await this.handleResponse<{ items: Todo[] } | Todo[]>(response);
    // Handle both paginated response {items: [...]} and direct array
    return Array.isArray(data) ? data : (data?.items || []);
  }

  /**
   * Get a single todo by ID
   * [Task]: AUTH-C5 - Now includes JWT token in Authorization header
   */
  async getTodo(id: number): Promise<Todo> {
    const response = await fetch(`${this.baseUrl}/api/todos/${id}`, {
      cache: 'no-store',
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<Todo>(response);
  }

  /**
   * Create a new todo
   * [Task]: AUTH-C5 - Now includes JWT token in Authorization header
   */
  async createTodo(data: TodoCreate): Promise<Todo> {
    const response = await fetch(`${this.baseUrl}/api/todos`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    return this.handleResponse<Todo>(response);
  }

  /**
   * Update an existing todo (partial update)
   * [Task]: AUTH-C5 - Now includes JWT token in Authorization header
   */
  async updateTodo(id: number, data: TodoUpdate): Promise<Todo> {
    const response = await fetch(`${this.baseUrl}/api/todos/${id}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    return this.handleResponse<Todo>(response);
  }

  /**
   * Delete a todo
   * [Task]: AUTH-C5 - Now includes JWT token in Authorization header
   */
  async deleteTodo(id: number): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/todos/${id}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<void>(response);
  }
}

/**
 * Create an authenticated API client with JWT token.
 * [Task]: AUTH-C5 - Helper function for creating authenticated API instances
 *
 * @param token - JWT token from Better Auth session
 * @returns TodoApi instance configured with authentication
 *
 * Example:
 *   // In a React component
 *   const { data: session } = useSession();
 *   const api = createAuthenticatedApi(session?.accessToken);
 *   const todos = await api.listTodos();
 */
export function createAuthenticatedApi(token: string | null): TodoApi {
  return new TodoApi(API_BASE_URL, token);
}

// Export singleton instance (call setToken() before using)
export const todoApi = new TodoApi();
