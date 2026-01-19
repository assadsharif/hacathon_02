/**
 * View/Edit Todo Page
 * Facebook-style design with inline styles
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { createAuthenticatedApi, Todo, TodoUpdate } from '@/lib/api';

interface User {
  id: string;
  name: string;
  email: string;
}

export default function TodoDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [todo, setTodo] = useState<Todo | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<'active' | 'completed'>('active');
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const todoId = parseInt(params.id);

  // Load user from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token');
    const storedUser = localStorage.getItem('user');

    if (!storedToken || !storedUser) {
      router.push('/sign-in');
      return;
    }

    setToken(storedToken);
    setUser(JSON.parse(storedUser));
  }, [router]);

  useEffect(() => {
    if (!token || isNaN(todoId)) return;

    const loadTodo = async () => {
      try {
        setIsLoading(true);
        setError('');
        const api = createAuthenticatedApi(token);
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
  }, [token, todoId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const api = createAuthenticatedApi(token);
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
    try {
      const api = createAuthenticatedApi(token);
      await api.deleteTodo(todoId);
      router.push('/todos');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo');
      setShowDeleteConfirm(false);
    }
  };

  const toggleStatus = async () => {
    if (!todo) return;

    try {
      const api = createAuthenticatedApi(token);
      const newStatus = todo.status === 'active' ? 'completed' : 'active';
      const updated = await api.updateTodo(todoId, { status: newStatus });
      setTodo(updated);
      setStatus(newStatus);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update status');
    }
  };

  // Loading spinner component
  const Spinner = () => (
    <>
      <div style={{
        width: '40px',
        height: '40px',
        border: '4px solid #e7f3ff',
        borderTopColor: '#1877f2',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite'
      }} />
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </>
  );

  if (!user || !token) {
    return (
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#f0f2f5',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <Spinner />
      </div>
    );
  }

  if (isLoading) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
        <header style={{ backgroundColor: '#1877f2', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
          <div style={{ maxWidth: '680px', margin: '0 auto', padding: '0 16px', height: '56px', display: 'flex', alignItems: 'center' }}>
            <Link href="/todos" style={{ fontSize: '24px', fontWeight: 'bold', color: '#ffffff', textDecoration: 'none' }}>
              Todo App
            </Link>
          </div>
        </header>
        <div style={{ textAlign: 'center', padding: '80px 0' }}>
          <div style={{ display: 'inline-block' }}><Spinner /></div>
          <p style={{ marginTop: '16px', color: '#65676b' }}>Loading todo...</p>
        </div>
      </div>
    );
  }

  if (error && !todo) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
        <header style={{ backgroundColor: '#1877f2', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
          <div style={{ maxWidth: '680px', margin: '0 auto', padding: '0 16px', height: '56px', display: 'flex', alignItems: 'center' }}>
            <Link href="/todos" style={{ fontSize: '24px', fontWeight: 'bold', color: '#ffffff', textDecoration: 'none' }}>
              Todo App
            </Link>
          </div>
        </header>
        <main style={{ maxWidth: '680px', margin: '0 auto', padding: '24px 16px' }}>
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '48px',
            textAlign: 'center',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
          }}>
            <div style={{
              width: '80px',
              height: '80px',
              backgroundColor: '#ffebe8',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 20px',
              fontSize: '32px'
            }}>
              !
            </div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1c1e21', marginBottom: '8px' }}>
              Todo not found
            </h3>
            <p style={{ color: '#65676b', marginBottom: '20px' }}>{error}</p>
            <Link
              href="/todos"
              style={{
                display: 'inline-block',
                padding: '12px 24px',
                backgroundColor: '#1877f2',
                color: '#ffffff',
                borderRadius: '6px',
                textDecoration: 'none',
                fontWeight: '600'
              }}
            >
              Back to Todos
            </Link>
          </div>
        </main>
      </div>
    );
  }

  if (!todo) return null;

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div style={{
          position: 'fixed',
          inset: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '24px',
            maxWidth: '400px',
            width: '90%',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
          }}>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1c1e21', marginBottom: '12px' }}>
              Delete Todo?
            </h3>
            <p style={{ color: '#65676b', marginBottom: '24px' }}>
              Are you sure you want to delete &quot;{todo.title}&quot;? This action cannot be undone.
            </p>
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
              <button
                onClick={() => setShowDeleteConfirm(false)}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#e4e6eb',
                  color: '#1c1e21',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#dd3c10',
                  color: '#ffffff',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <header style={{
        backgroundColor: '#1877f2',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
      }}>
        <div style={{
          maxWidth: '680px',
          margin: '0 auto',
          padding: '0 16px',
          height: '56px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <Link href="/todos" style={{
            fontSize: '24px',
            fontWeight: 'bold',
            color: '#ffffff',
            textDecoration: 'none'
          }}>
            Todo App
          </Link>
          {!isEditing && (
            <button
              onClick={() => setIsEditing(true)}
              style={{
                padding: '8px 16px',
                backgroundColor: '#ffffff',
                color: '#1877f2',
                borderRadius: '6px',
                border: 'none',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '600'
              }}
            >
              Edit
            </button>
          )}
        </div>
      </header>

      <main style={{ maxWidth: '680px', margin: '0 auto', padding: '24px 16px' }}>
        {/* Back Link */}
        <Link
          href="/todos"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            color: '#1877f2',
            textDecoration: 'none',
            fontSize: '14px',
            marginBottom: '24px'
          }}
        >
          <span style={{ fontSize: '18px' }}>&larr;</span>
          Back to todos
        </Link>

        {/* Error */}
        {error && (
          <div style={{
            backgroundColor: '#ffebe8',
            border: '1px solid #dd3c10',
            borderRadius: '8px',
            padding: '12px 16px',
            marginBottom: '24px',
            color: '#dd3c10',
            fontSize: '14px'
          }}>
            {error}
          </div>
        )}

        {/* View Mode */}
        {!isEditing && (
          <>
            {/* Todo Card */}
            <div style={{
              backgroundColor: '#ffffff',
              borderRadius: '8px',
              boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
              overflow: 'hidden'
            }}>
              <div style={{ padding: '24px' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                  {/* Checkbox */}
                  <button
                    onClick={toggleStatus}
                    style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '50%',
                      border: todo.status === 'completed' ? 'none' : '3px solid #bec3c9',
                      backgroundColor: todo.status === 'completed' ? '#42b72a' : 'transparent',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}
                  >
                    {todo.status === 'completed' && (
                      <span style={{ color: '#ffffff', fontSize: '18px', fontWeight: 'bold' }}>✓</span>
                    )}
                  </button>

                  {/* Content */}
                  <div style={{ flex: 1 }}>
                    <h1 style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: todo.status === 'completed' ? '#bec3c9' : '#1c1e21',
                      textDecoration: todo.status === 'completed' ? 'line-through' : 'none',
                      marginBottom: '8px'
                    }}>
                      {todo.title}
                    </h1>
                    {todo.description && (
                      <p style={{
                        fontSize: '16px',
                        color: todo.status === 'completed' ? '#bec3c9' : '#65676b',
                        lineHeight: '1.5',
                        whiteSpace: 'pre-wrap'
                      }}>
                        {todo.description}
                      </p>
                    )}
                  </div>
                </div>
              </div>

              {/* Footer */}
              <div style={{
                padding: '16px 24px',
                backgroundColor: '#f7f8fa',
                borderTop: '1px solid #e4e6eb',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div style={{ fontSize: '13px', color: '#65676b' }}>
                  Created {new Date(todo.created_at).toLocaleDateString('en-US', {
                    weekday: 'short',
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                  })}
                  {todo.updated_at !== todo.created_at && (
                    <> · Updated {new Date(todo.updated_at).toLocaleDateString('en-US', {
                      month: 'short',
                      day: 'numeric'
                    })}</>
                  )}
                </div>
                <span style={{
                  padding: '6px 12px',
                  borderRadius: '20px',
                  fontSize: '12px',
                  fontWeight: '600',
                  backgroundColor: todo.status === 'completed' ? '#d4edda' : '#e7f3ff',
                  color: todo.status === 'completed' ? '#28a745' : '#1877f2',
                  textTransform: 'capitalize'
                }}>
                  {todo.status}
                </span>
              </div>
            </div>

            {/* Action Buttons */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '12px',
              marginTop: '24px'
            }}>
              <button
                onClick={toggleStatus}
                style={{
                  padding: '14px 24px',
                  backgroundColor: '#ffffff',
                  color: '#1c1e21',
                  border: '1px solid #ccd0d5',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '15px',
                  fontWeight: '600'
                }}
              >
                Mark as {todo.status === 'active' ? 'Completed' : 'Active'}
              </button>
              <button
                onClick={() => setShowDeleteConfirm(true)}
                style={{
                  padding: '14px 24px',
                  backgroundColor: '#ffebe8',
                  color: '#dd3c10',
                  border: '1px solid #dd3c10',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '15px',
                  fontWeight: '600'
                }}
              >
                Delete Todo
              </button>
            </div>
          </>
        )}

        {/* Edit Mode */}
        {isEditing && (
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
            overflow: 'hidden'
          }}>
            {/* Card Header */}
            <div style={{
              padding: '20px 24px',
              borderBottom: '1px solid #e4e6eb'
            }}>
              <h1 style={{
                fontSize: '24px',
                fontWeight: 'bold',
                color: '#1c1e21',
                margin: 0
              }}>
                Edit Todo
              </h1>
            </div>

            {/* Card Body */}
            <div style={{ padding: '24px' }}>
              <form onSubmit={handleSubmit}>
                {/* Title */}
                <div style={{ marginBottom: '20px' }}>
                  <label
                    htmlFor="title"
                    style={{
                      display: 'block',
                      fontSize: '14px',
                      fontWeight: '600',
                      color: '#1c1e21',
                      marginBottom: '8px'
                    }}
                  >
                    Title <span style={{ color: '#dd3c10' }}>*</span>
                  </label>
                  <input
                    id="title"
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      fontSize: '16px',
                      border: '1px solid #ccd0d5',
                      borderRadius: '6px',
                      outline: 'none',
                      backgroundColor: '#f5f6f7',
                      color: '#1c1e21',
                      boxSizing: 'border-box'
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = '#1877f2';
                      e.target.style.backgroundColor = '#ffffff';
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = '#ccd0d5';
                      e.target.style.backgroundColor = '#f5f6f7';
                    }}
                  />
                </div>

                {/* Description */}
                <div style={{ marginBottom: '20px' }}>
                  <label
                    htmlFor="description"
                    style={{
                      display: 'block',
                      fontSize: '14px',
                      fontWeight: '600',
                      color: '#1c1e21',
                      marginBottom: '8px'
                    }}
                  >
                    Description
                  </label>
                  <textarea
                    id="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      fontSize: '16px',
                      border: '1px solid #ccd0d5',
                      borderRadius: '6px',
                      outline: 'none',
                      backgroundColor: '#f5f6f7',
                      color: '#1c1e21',
                      resize: 'vertical',
                      minHeight: '100px',
                      boxSizing: 'border-box',
                      fontFamily: 'inherit'
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = '#1877f2';
                      e.target.style.backgroundColor = '#ffffff';
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = '#ccd0d5';
                      e.target.style.backgroundColor = '#f5f6f7';
                    }}
                  />
                </div>

                {/* Status */}
                <div style={{ marginBottom: '24px' }}>
                  <label style={{
                    display: 'block',
                    fontSize: '14px',
                    fontWeight: '600',
                    color: '#1c1e21',
                    marginBottom: '12px'
                  }}>
                    Status
                  </label>
                  <div style={{ display: 'flex', gap: '16px' }}>
                    <label style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      cursor: 'pointer',
                      padding: '12px 20px',
                      borderRadius: '6px',
                      border: status === 'active' ? '2px solid #1877f2' : '2px solid #e4e6eb',
                      backgroundColor: status === 'active' ? '#e7f3ff' : '#ffffff'
                    }}>
                      <input
                        type="radio"
                        name="status"
                        value="active"
                        checked={status === 'active'}
                        onChange={() => setStatus('active')}
                        style={{ display: 'none' }}
                      />
                      <span style={{
                        width: '20px',
                        height: '20px',
                        borderRadius: '50%',
                        border: status === 'active' ? '6px solid #1877f2' : '2px solid #bec3c9',
                        backgroundColor: '#ffffff'
                      }} />
                      <span style={{
                        fontWeight: '600',
                        color: status === 'active' ? '#1877f2' : '#65676b'
                      }}>Active</span>
                    </label>
                    <label style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      cursor: 'pointer',
                      padding: '12px 20px',
                      borderRadius: '6px',
                      border: status === 'completed' ? '2px solid #42b72a' : '2px solid #e4e6eb',
                      backgroundColor: status === 'completed' ? '#d4edda' : '#ffffff'
                    }}>
                      <input
                        type="radio"
                        name="status"
                        value="completed"
                        checked={status === 'completed'}
                        onChange={() => setStatus('completed')}
                        style={{ display: 'none' }}
                      />
                      <span style={{
                        width: '20px',
                        height: '20px',
                        borderRadius: '50%',
                        border: status === 'completed' ? '6px solid #42b72a' : '2px solid #bec3c9',
                        backgroundColor: '#ffffff'
                      }} />
                      <span style={{
                        fontWeight: '600',
                        color: status === 'completed' ? '#42b72a' : '#65676b'
                      }}>Completed</span>
                    </label>
                  </div>
                </div>

                {/* Buttons */}
                <div style={{
                  display: 'flex',
                  gap: '12px',
                  paddingTop: '16px',
                  borderTop: '1px solid #e4e6eb'
                }}>
                  <button
                    type="submit"
                    disabled={isSubmitting || !title.trim()}
                    style={{
                      flex: 1,
                      padding: '12px 24px',
                      fontSize: '16px',
                      fontWeight: 'bold',
                      backgroundColor: isSubmitting || !title.trim() ? '#bec3c9' : '#1877f2',
                      color: '#ffffff',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: isSubmitting || !title.trim() ? 'not-allowed' : 'pointer'
                    }}
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
                    style={{
                      padding: '12px 24px',
                      fontSize: '16px',
                      fontWeight: '600',
                      backgroundColor: '#e4e6eb',
                      color: '#1c1e21',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer'
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
