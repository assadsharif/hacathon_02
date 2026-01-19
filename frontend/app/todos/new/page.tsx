/**
 * Create New Todo Page
 * Facebook-style design with inline styles
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
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

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
        status: 'active',
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
      <div style={{
        minHeight: '100vh',
        backgroundColor: '#f0f2f5',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{
          width: '40px',
          height: '40px',
          border: '4px solid #e7f3ff',
          borderTopColor: '#1877f2',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
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

        {/* Form Card */}
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
              Create New Todo
            </h1>
            <p style={{
              fontSize: '14px',
              color: '#65676b',
              marginTop: '4px'
            }}>
              Add a new task to your list
            </p>
          </div>

          {/* Card Body */}
          <div style={{ padding: '24px' }}>
            <form onSubmit={handleSubmit}>
              {/* Error */}
              {error && (
                <div style={{
                  backgroundColor: '#ffebe8',
                  border: '1px solid #dd3c10',
                  borderRadius: '8px',
                  padding: '12px 16px',
                  marginBottom: '20px',
                  color: '#dd3c10',
                  fontSize: '14px'
                }}>
                  {error}
                </div>
              )}

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
                  placeholder="What needs to be done?"
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
              <div style={{ marginBottom: '24px' }}>
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
                  Description <span style={{ color: '#65676b', fontWeight: 'normal' }}>(optional)</span>
                </label>
                <textarea
                  id="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={4}
                  placeholder="Add more details about this task..."
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
                  {isSubmitting ? 'Creating...' : 'Create Todo'}
                </button>
                <Link
                  href="/todos"
                  style={{
                    padding: '12px 24px',
                    fontSize: '16px',
                    fontWeight: '600',
                    backgroundColor: '#e4e6eb',
                    color: '#1c1e21',
                    border: 'none',
                    borderRadius: '6px',
                    textDecoration: 'none',
                    textAlign: 'center'
                  }}
                >
                  Cancel
                </Link>
              </div>
            </form>
          </div>
        </div>

        {/* Tips Card */}
        <div style={{
          marginTop: '24px',
          backgroundColor: '#e7f3ff',
          borderRadius: '8px',
          padding: '16px 20px',
          border: '1px solid #b3d4fc'
        }}>
          <h3 style={{
            fontSize: '14px',
            fontWeight: '600',
            color: '#1877f2',
            marginBottom: '8px'
          }}>
            Tips for effective todos
          </h3>
          <ul style={{
            margin: 0,
            paddingLeft: '20px',
            color: '#1c1e21',
            fontSize: '14px',
            lineHeight: '1.6'
          }}>
            <li>Be specific about what needs to be done</li>
            <li>Break large tasks into smaller ones</li>
            <li>Add descriptions for complex tasks</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
