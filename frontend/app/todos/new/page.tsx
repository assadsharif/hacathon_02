/**
 * Create New Todo Page
 * Allows authenticated users to create a new todo
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useSession } from '@/lib/auth-client';
import { createAuthenticatedApi, TodoCreate } from '@/lib/api';

export default function NewTodoPage() {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<'active' | 'completed'>('active');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Redirect to sign-in if not authenticated
  useEffect(() => {
    if (!isPending && !session) {
      router.push('/sign-in');
    }
  }, [session, isPending, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const api = createAuthenticatedApi(session?.session?.token || null);
      const todoData: TodoCreate = {
        title,
        description: description || null,
        status,
      };

      await api.createTodo(todoData);
      router.push('/todos');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create todo');
      setIsSubmitting(false);
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
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
              Create New Todo
            </h1>
            <p className="text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
              Add a new task to your list
            </p>
          </div>

          {/* Form Card */}
          <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4">
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
                  Description (optional)
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
                  {isSubmitting ? 'Creating...' : 'Create Todo'}
                </button>
                <Link
                  href="/todos"
                  className="flex-1 py-3.5 px-6 rounded-xl text-gray-700 font-semibold bg-gray-100 hover:bg-gray-200 transition-all text-center"
                  style={{ fontFamily: 'DM Sans, sans-serif' }}
                >
                  Cancel
                </Link>
              </div>
            </form>
          </div>

          {/* Help Text */}
          <div className="mt-6 text-center text-sm text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
            <p>Press Escape to cancel or use Ctrl+Enter to submit</p>
          </div>
        </div>
      </div>
    </>
  );
}
