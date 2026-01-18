/**
 * View/Edit Todo Page
 * Displays and allows editing of a single todo
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useSession } from '@/lib/auth-client';
import { createAuthenticatedApi, Todo, TodoUpdate } from '@/lib/api';

export default function TodoDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const [todo, setTodo] = useState<Todo | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<'active' | 'completed'>('active');
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  const todoId = parseInt(params.id);

  // Redirect to sign-in if not authenticated
  useEffect(() => {
    if (!isPending && !session) {
      router.push('/sign-in');
    }
  }, [session, isPending, router]);

  // Load todo
  useEffect(() => {
    if (!session || isNaN(todoId)) return;

    const loadTodo = async () => {
      try {
        setIsLoading(true);
        setError('');
        const api = createAuthenticatedApi(session.session?.token || null);
        const data = await api.getTodo(todoId);
        setTodo(data);
        setTitle(data.title);
        setDescription(data.description || '');
        setStatus(data.status);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load todo');
      } finally {
        setIsLoading(false);
      }
    };

    loadTodo();
  }, [session, todoId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const api = createAuthenticatedApi(session?.session?.token || null);
      const updateData: TodoUpdate = {
        title,
        description: description || null,
        status,
      };

      const updated = await api.updateTodo(todoId, updateData);
      setTodo(updated);
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update todo');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this todo?')) return;

    try {
      const api = createAuthenticatedApi(session?.session?.token || null);
      await api.deleteTodo(todoId);
      router.push('/todos');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo');
    }
  };

  const toggleStatus = async () => {
    if (!todo) return;

    try {
      const api = createAuthenticatedApi(session?.session?.token || null);
      const newStatus = todo.status === 'active' ? 'completed' : 'active';
      const updated = await api.updateTodo(todoId, { status: newStatus });
      setTodo(updated);
      setStatus(newStatus);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update status');
    }
  };

  if (isPending || !session) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent"></div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 py-8">
        <div className="max-w-2xl mx-auto px-4">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent mx-auto"></div>
            <p className="mt-4 text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
              Loading todo...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (error && !todo) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 py-8">
        <div className="max-w-2xl mx-auto px-4">
          <div className="bg-red-50 border border-red-200 rounded-xl p-8 text-center">
            <svg className="w-12 h-12 text-red-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="text-xl font-bold text-red-900 mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
              Failed to load todo
            </h3>
            <p className="text-red-700 mb-6" style={{ fontFamily: 'DM Sans, sans-serif' }}>
              {error}
            </p>
            <Link
              href="/todos"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-500 text-white px-6 py-3 rounded-lg font-semibold"
              style={{ fontFamily: 'DM Sans, sans-serif' }}
            >
              Back to todos
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (!todo) return null;

  return (
    <>
      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

        .input-field-todo {
          transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
          border: 2px solid rgba(107, 70, 193, 0.15);
          background: rgba(255, 255, 255, 0.9);
        }

        .input-field-todo:focus {
          outline: none;
          border-color: #7B68EE;
          background: rgba(255, 255, 255, 1);
          box-shadow:
            0 0 0 4px rgba(123, 104, 238, 0.1),
            0 4px 12px rgba(123, 104, 238, 0.15);
          transform: translateY(-1px);
        }

        .btn-primary-todo {
          background: linear-gradient(135deg, #7B68EE 0%, #C471ED 100%);
          transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
          box-shadow:
            0 4px 16px rgba(123, 104, 238, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        }

        .btn-primary-todo:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow:
            0 8px 24px rgba(123, 104, 238, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset;
        }

        .btn-primary-todo:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }
      `}</style>

      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 py-8">
        <div className="max-w-2xl mx-auto px-4">
          {/* Back Button */}
          <Link
            href="/todos"
            className="inline-flex items-center gap-2 text-gray-600 hover:text-purple-600 mb-6 transition-colors"
            style={{ fontFamily: 'DM Sans, sans-serif' }}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to todos
          </Link>

          {/* Header */}
          <div className="mb-6 flex items-start justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
                {isEditing ? 'Edit Todo' : 'Todo Details'}
              </h1>
              <div className="flex items-center gap-4 text-sm text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                <span>Created: {new Date(todo.created_at).toLocaleDateString()}</span>
                {todo.updated_at !== todo.created_at && (
                  <span>Updated: {new Date(todo.updated_at).toLocaleDateString()}</span>
                )}
              </div>
            </div>
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="bg-gradient-to-r from-purple-600 to-pink-500 text-white px-5 py-2.5 rounded-lg font-semibold shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all inline-flex items-center gap-2"
                style={{ fontFamily: 'DM Sans, sans-serif' }}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Edit
              </button>
            )}
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <p className="text-sm font-medium text-red-800" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                  {error}
                </p>
              </div>
            </div>
          )}

          {/* View Mode */}
          {!isEditing && (
            <div className="space-y-6">
              {/* Main Card */}
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8">
                <div className="mb-6">
                  <div className="flex items-start gap-4 mb-4">
                    <button
                      onClick={toggleStatus}
                      className={`flex-shrink-0 w-8 h-8 rounded-lg border-2 transition-all ${
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
                    <h2
                      className={`text-3xl font-bold ${
                        todo.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900'
                      }`}
                      style={{ fontFamily: 'Outfit, sans-serif' }}
                    >
                      {todo.title}
                    </h2>
                  </div>

                  {todo.description && (
                    <div className="ml-12">
                      <p
                        className={`text-lg ${
                          todo.status === 'completed' ? 'text-gray-400' : 'text-gray-700'
                        }`}
                        style={{ fontFamily: 'DM Sans, sans-serif' }}
                      >
                        {todo.description}
                      </p>
                    </div>
                  )}
                </div>

                <div className="ml-12 pt-4 border-t border-gray-200">
                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-purple-100 to-pink-100">
                    <span
                      className={`w-2 h-2 rounded-full ${
                        todo.status === 'completed' ? 'bg-green-500' : 'bg-purple-500'
                      }`}
                    ></span>
                    <span className="text-sm font-semibold text-gray-700 capitalize" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                      {todo.status}
                    </span>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-4">
                <button
                  onClick={toggleStatus}
                  className="flex-1 py-3 px-6 rounded-xl font-semibold bg-white/90 hover:bg-white text-gray-700 border-2 border-gray-200 hover:border-purple-300 transition-all"
                  style={{ fontFamily: 'DM Sans, sans-serif' }}
                >
                  Mark as {todo.status === 'active' ? 'Completed' : 'Active'}
                </button>
                <button
                  onClick={handleDelete}
                  className="py-3 px-6 rounded-xl font-semibold bg-red-500 hover:bg-red-600 text-white transition-all"
                  style={{ fontFamily: 'DM Sans, sans-serif' }}
                >
                  Delete
                </button>
              </div>
            </div>
          )}

          {/* Edit Mode */}
          {isEditing && (
            <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Title Field */}
                <div>
                  <label htmlFor="title" className="block text-sm font-semibold text-gray-700 mb-2" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                    Title *
                  </label>
                  <input
                    id="title"
                    name="title"
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="input-field-todo block w-full px-4 py-3 rounded-xl text-gray-900 placeholder-gray-400"
                    placeholder="What needs to be done?"
                    style={{ fontFamily: 'DM Sans, sans-serif' }}
                    maxLength={200}
                  />
                  <p className="mt-1 text-xs text-gray-500" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                    {title.length}/200 characters
                  </p>
                </div>

                {/* Description Field */}
                <div>
                  <label htmlFor="description" className="block text-sm font-semibold text-gray-700 mb-2" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                    Description
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    className="input-field-todo block w-full px-4 py-3 rounded-xl text-gray-900 placeholder-gray-400 resize-none"
                    placeholder="Add more details about this todo..."
                    style={{ fontFamily: 'DM Sans, sans-serif' }}
                  />
                </div>

                {/* Status Field */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                    Status
                  </label>
                  <div className="flex gap-4">
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="status"
                        value="active"
                        checked={status === 'active'}
                        onChange={() => setStatus('active')}
                        className="w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
                      />
                      <span className="ml-2 text-gray-700" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                        Active
                      </span>
                    </label>
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="status"
                        value="completed"
                        checked={status === 'completed'}
                        onChange={() => setStatus('completed')}
                        className="w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
                      />
                      <span className="ml-2 text-gray-700" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                        Completed
                      </span>
                    </label>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 pt-4">
                  <button
                    type="submit"
                    disabled={isSubmitting || !title.trim()}
                    className="btn-primary-todo flex-1 py-3.5 px-6 rounded-xl text-white font-semibold"
                    style={{ fontFamily: 'DM Sans, sans-serif' }}
                  >
                    {isSubmitting ? 'Saving...' : 'Save Changes'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setIsEditing(false);
                      setTitle(todo.title);
                      setDescription(todo.description || '');
                      setStatus(todo.status);
                      setError('');
                    }}
                    className="flex-1 py-3.5 px-6 rounded-xl text-gray-700 font-semibold bg-gray-100 hover:bg-gray-200 transition-all"
                    style={{ fontFamily: 'DM Sans, sans-serif' }}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
