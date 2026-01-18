/**
 * Todo List Page
 * Displays all todos for the authenticated user with filtering and CRUD operations
 */

'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useSession } from '@/lib/auth-client';
import { createAuthenticatedApi, Todo } from '@/lib/api';

export default function TodosPage() {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  // Redirect to sign-in if not authenticated
  useEffect(() => {
    if (!isPending && !session) {
      router.push('/sign-in');
    }
  }, [session, isPending, router]);

  // Load todos
  useEffect(() => {
    if (!session) return;

    const loadTodos = async () => {
      try {
        setIsLoading(true);
        setError('');
        const api = createAuthenticatedApi(session.session?.token || null);
        const statusFilter = filter === 'all' ? undefined : filter;
        const data = await api.listTodos(statusFilter);
        setTodos(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load todos');
      } finally {
        setIsLoading(false);
      }
    };

    loadTodos();
  }, [session, filter]);

  const toggleTodoStatus = async (todo: Todo) => {
    try {
      const api = createAuthenticatedApi(session?.session?.token || null);
      const newStatus = todo.status === 'active' ? 'completed' : 'active';
      await api.updateTodo(todo.id, { status: newStatus });

      // Update local state
      setTodos(todos.map(t =>
        t.id === todo.id ? { ...t, status: newStatus } : t
      ));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update todo');
    }
  };

  const deleteTodo = async (id: number) => {
    if (!confirm('Are you sure you want to delete this todo?')) return;

    try {
      const api = createAuthenticatedApi(session?.session?.token || null);
      await api.deleteTodo(id);
      setTodos(todos.filter(t => t.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo');
    }
  };

  if (isPending || !session) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <>
      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
      `}</style>

      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
              My Todos
            </h1>
            <p className="text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
              Manage your tasks efficiently
            </p>
          </div>

          {/* Actions Bar */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-6 mb-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              {/* Filter Tabs */}
              <div className="flex gap-2">
                <button
                  onClick={() => setFilter('all')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    filter === 'all'
                      ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                  style={{ fontFamily: 'DM Sans, sans-serif' }}
                >
                  All ({todos.length})
                </button>
                <button
                  onClick={() => setFilter('active')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    filter === 'active'
                      ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                  style={{ fontFamily: 'DM Sans, sans-serif' }}
                >
                  Active
                </button>
                <button
                  onClick={() => setFilter('completed')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    filter === 'completed'
                      ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white shadow-md'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                  style={{ fontFamily: 'DM Sans, sans-serif' }}
                >
                  Completed
                </button>
              </div>

              {/* Create Button */}
              <Link
                href="/todos/new"
                className="bg-gradient-to-r from-purple-600 to-pink-500 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all inline-flex items-center gap-2"
                style={{ fontFamily: 'DM Sans, sans-serif' }}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                New Todo
              </Link>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
              <p className="text-red-800 text-sm font-medium" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                {error}
              </p>
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent mx-auto"></div>
              <p className="mt-4 text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                Loading todos...
              </p>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && todos.length === 0 && (
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-12 text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
                No todos yet
              </h3>
              <p className="text-gray-600 mb-6" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                Get started by creating your first todo!
              </p>
              <Link
                href="/todos/new"
                className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-500 text-white px-6 py-3 rounded-lg font-semibold shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all"
                style={{ fontFamily: 'DM Sans, sans-serif' }}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Create Todo
              </Link>
            </div>
          )}

          {/* Todo List */}
          {!isLoading && todos.length > 0 && (
            <div className="space-y-3">
              {todos.map((todo) => (
                <div
                  key={todo.id}
                  className="bg-white/80 backdrop-blur-sm rounded-xl shadow-md hover:shadow-lg transition-all p-5 group"
                >
                  <div className="flex items-start gap-4">
                    {/* Checkbox */}
                    <button
                      onClick={() => toggleTodoStatus(todo)}
                      className={`flex-shrink-0 w-6 h-6 rounded-lg border-2 transition-all ${
                        todo.status === 'completed'
                          ? 'bg-gradient-to-br from-purple-500 to-pink-500 border-transparent'
                          : 'border-gray-300 hover:border-purple-400'
                      }`}
                    >
                      {todo.status === 'completed' && (
                        <svg className="w-full h-full text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                        </svg>
                      )}
                    </button>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <Link href={`/todos/${todo.id}`}>
                        <h3
                          className={`text-lg font-semibold mb-1 hover:text-purple-600 transition-colors ${
                            todo.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900'
                          }`}
                          style={{ fontFamily: 'Outfit, sans-serif' }}
                        >
                          {todo.title}
                        </h3>
                      </Link>
                      {todo.description && (
                        <p
                          className={`text-sm mb-2 ${
                            todo.status === 'completed' ? 'text-gray-400' : 'text-gray-600'
                          }`}
                          style={{ fontFamily: 'DM Sans, sans-serif' }}
                        >
                          {todo.description}
                        </p>
                      )}
                      <div className="flex items-center gap-4 text-xs text-gray-500" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                        <span>Created: {new Date(todo.created_at).toLocaleDateString()}</span>
                        {todo.updated_at !== todo.created_at && (
                          <span>Updated: {new Date(todo.updated_at).toLocaleDateString()}</span>
                        )}
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Link
                        href={`/todos/${todo.id}`}
                        className="p-2 text-gray-600 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
                        title="Edit"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </Link>
                      <button
                        onClick={() => deleteTodo(todo.id)}
                        className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Delete"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
