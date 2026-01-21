/**
 * Todo List Page
 * Facebook-style design with inline styles
 * [Task]: T054 - Added WebSocket real-time sync
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { createAuthenticatedApi, Todo } from '@/lib/api';
import { useTaskWebSocket } from '@/hooks/useTaskWebSocket';

interface User {
  id: string;
  name: string;
  email: string;
}

export default function TodosPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showUserMenu, setShowUserMenu] = useState(false);

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

  // Load todos function
  const loadTodos = useCallback(async () => {
    if (!token) return;
    try {
      setIsLoading(true);
      setError('');
      const api = createAuthenticatedApi(token);
      const statusFilter = filter === 'all' ? undefined : filter;
      const data = await api.listTodos(statusFilter);
      setTodos(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load todos');
    } finally {
      setIsLoading(false);
    }
  }, [token, filter]);

  // Load todos when token is available
  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  // [Task]: T054 - WebSocket real-time sync
  const { isConnected } = useTaskWebSocket(token, {
    onTaskCreated: () => loadTodos(),
    onTaskUpdated: () => loadTodos(),
    onTaskCompleted: () => loadTodos(),
    onTaskDeleted: () => loadTodos(),
    onReminderTriggered: (data) => {
      // Show notification for reminder
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Task Reminder', {
          body: data.title || 'You have a task due!',
          icon: '/favicon.ico'
        });
      }
    }
  });

  const toggleTodoStatus = async (todo: Todo) => {
    try {
      const api = createAuthenticatedApi(token);
      const newStatus = todo.status === 'active' ? 'completed' : 'active';
      await api.updateTodo(todo.id, { status: newStatus });
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
      const api = createAuthenticatedApi(token);
      await api.deleteTodo(id);
      setTodos(todos.filter(t => t.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo');
    }
  };

  const handleSignOut = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    router.push('/sign-in');
  };

  if (!user || !token) {
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

  const filteredTodos = todos
    .filter(t => filter === 'all' || t.status === filter)
    .filter(t =>
      searchQuery === '' ||
      t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (t.description && t.description.toLowerCase().includes(searchQuery.toLowerCase()))
    );

  const activeTodos = todos.filter(t => t.status === 'active').length;
  const completedTodos = todos.filter(t => t.status === 'completed').length;

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
      {/* Header */}
      <header style={{
        backgroundColor: '#1877f2',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <div style={{
          maxWidth: '960px',
          margin: '0 auto',
          padding: '0 16px',
          height: '56px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <Link href="/" style={{
            fontSize: '24px',
            fontWeight: 'bold',
            color: '#ffffff',
            textDecoration: 'none'
          }}>
            Todo App
          </Link>

          {/* Search Bar */}
          <div style={{
            flex: 1,
            maxWidth: '400px',
            margin: '0 20px'
          }}>
            <input
              type="text"
              placeholder="Search todos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 16px',
                borderRadius: '20px',
                border: 'none',
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                color: '#ffffff',
                fontSize: '14px',
                outline: 'none'
              }}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Link
              href="/todos/new"
              style={{
                padding: '8px 16px',
                backgroundColor: '#42b72a',
                color: '#ffffff',
                borderRadius: '6px',
                textDecoration: 'none',
                fontSize: '14px',
                fontWeight: '600'
              }}
            >
              + New Todo
            </Link>

            {/* User Menu */}
            <div style={{ position: 'relative' }}>
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '50%',
                  backgroundColor: '#ffffff',
                  border: 'none',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '16px',
                  fontWeight: 'bold',
                  color: '#1877f2'
                }}
              >
                {user?.name?.[0]?.toUpperCase() || 'U'}
              </button>

              {showUserMenu && (
                <div style={{
                  position: 'absolute',
                  top: '100%',
                  right: 0,
                  marginTop: '8px',
                  backgroundColor: '#ffffff',
                  borderRadius: '8px',
                  boxShadow: '0 2px 12px rgba(0, 0, 0, 0.15)',
                  minWidth: '200px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    padding: '12px 16px',
                    borderBottom: '1px solid #e4e6eb'
                  }}>
                    <p style={{ fontWeight: '600', color: '#1c1e21' }}>
                      {user?.name || 'User'}
                    </p>
                    <p style={{ fontSize: '13px', color: '#65676b' }}>
                      {user?.email}
                    </p>
                  </div>
                  <button
                    onClick={handleSignOut}
                    style={{
                      width: '100%',
                      padding: '12px 16px',
                      textAlign: 'left',
                      backgroundColor: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      fontSize: '14px',
                      color: '#1c1e21'
                    }}
                  >
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <main style={{ maxWidth: '960px', margin: '0 auto', padding: '24px 16px' }}>
        {/* Stats Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '16px',
          marginBottom: '24px'
        }}>
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
          }}>
            <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#1877f2' }}>
              {todos.length}
            </p>
            <p style={{ fontSize: '14px', color: '#65676b' }}>Total Tasks</p>
          </div>
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
          }}>
            <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#f5a623' }}>
              {activeTodos}
            </p>
            <p style={{ fontSize: '14px', color: '#65676b' }}>Active</p>
          </div>
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
          }}>
            <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#42b72a' }}>
              {completedTodos}
            </p>
            <p style={{ fontSize: '14px', color: '#65676b' }}>Completed</p>
          </div>
        </div>

        {/* Filter Tabs */}
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '8px',
          padding: '4px',
          marginBottom: '24px',
          display: 'inline-flex',
          boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)'
        }}>
          {(['all', 'active', 'completed'] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{
                padding: '10px 20px',
                borderRadius: '6px',
                border: 'none',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '600',
                backgroundColor: filter === f ? '#1877f2' : 'transparent',
                color: filter === f ? '#ffffff' : '#65676b',
                textTransform: 'capitalize',
                transition: 'all 0.2s'
              }}
            >
              {f}
            </button>
          ))}
        </div>

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

        {/* Loading */}
        {isLoading && (
          <div style={{ textAlign: 'center', padding: '48px 0' }}>
            <div style={{
              width: '40px',
              height: '40px',
              border: '4px solid #e7f3ff',
              borderTopColor: '#1877f2',
              borderRadius: '50%',
              margin: '0 auto',
              animation: 'spin 1s linear infinite'
            }} />
            <p style={{ marginTop: '16px', color: '#65676b' }}>Loading your todos...</p>
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
          </div>
        )}

        {/* Empty State */}
        {!isLoading && filteredTodos.length === 0 && (
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
              backgroundColor: '#e7f3ff',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 20px',
              fontSize: '32px'
            }}>
              {searchQuery ? '🔍' : '📝'}
            </div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1c1e21', marginBottom: '8px' }}>
              {searchQuery ? 'No results found' : 'No todos yet'}
            </h3>
            <p style={{ color: '#65676b', marginBottom: '20px' }}>
              {searchQuery
                ? `No todos match "${searchQuery}"`
                : filter === 'all'
                  ? 'Create your first todo to get started!'
                  : `No ${filter} todos.`
              }
            </p>
            {!searchQuery && filter === 'all' && (
              <Link
                href="/todos/new"
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
                Create Your First Todo
              </Link>
            )}
          </div>
        )}

        {/* Todo List */}
        {!isLoading && filteredTodos.length > 0 && (
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
            overflow: 'hidden'
          }}>
            {filteredTodos.map((todo, index) => (
              <div
                key={todo.id}
                style={{
                  padding: '16px 20px',
                  borderBottom: index < filteredTodos.length - 1 ? '1px solid #e4e6eb' : 'none',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '12px',
                  transition: 'background-color 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f7f8fa'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
              >
                {/* Checkbox */}
                <button
                  onClick={() => toggleTodoStatus(todo)}
                  style={{
                    width: '24px',
                    height: '24px',
                    borderRadius: '50%',
                    border: todo.status === 'completed' ? 'none' : '2px solid #bec3c9',
                    backgroundColor: todo.status === 'completed' ? '#42b72a' : 'transparent',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    marginTop: '2px'
                  }}
                >
                  {todo.status === 'completed' && (
                    <span style={{ color: '#ffffff', fontSize: '14px' }}>✓</span>
                  )}
                </button>

                {/* Content */}
                <div style={{ flex: 1, minWidth: 0 }}>
                  <Link href={`/todos/${todo.id}`} style={{ textDecoration: 'none' }}>
                    <h3 style={{
                      fontSize: '16px',
                      fontWeight: '600',
                      color: todo.status === 'completed' ? '#bec3c9' : '#1c1e21',
                      textDecoration: todo.status === 'completed' ? 'line-through' : 'none',
                      marginBottom: '4px'
                    }}>
                      {todo.title}
                    </h3>
                  </Link>
                  {todo.description && (
                    <p style={{
                      fontSize: '14px',
                      color: todo.status === 'completed' ? '#bec3c9' : '#65676b',
                      marginBottom: '8px',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap'
                    }}>
                      {todo.description}
                    </p>
                  )}
                  <p style={{ fontSize: '12px', color: '#8a8d91' }}>
                    {new Date(todo.created_at).toLocaleDateString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric'
                    })}
                  </p>
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', gap: '8px' }}>
                  <Link
                    href={`/todos/${todo.id}`}
                    style={{
                      padding: '8px',
                      borderRadius: '6px',
                      backgroundColor: '#e7f3ff',
                      color: '#1877f2',
                      textDecoration: 'none',
                      fontSize: '14px'
                    }}
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => deleteTodo(todo.id)}
                    style={{
                      padding: '8px 12px',
                      borderRadius: '6px',
                      backgroundColor: '#ffebe8',
                      color: '#dd3c10',
                      border: 'none',
                      cursor: 'pointer',
                      fontSize: '14px'
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
