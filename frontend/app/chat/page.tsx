/**
 * Chat Page - AI Todo Assistant Interface
 * [Task]: C1, C2, C3 - Chat UI integration
 * [Task]: T055 - WebSocket real-time sync
 * [Refs]: specs/phase-iii/plan.md#file-structure
 *
 * This page provides the conversational interface for managing todos
 * through natural language with the TodoAgent.
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { ChatWindow } from '@/components/chat';
import { useTaskWebSocket } from '@/hooks/useTaskWebSocket';

interface User {
  id: string;
  name: string;
  email: string;
}

export default function ChatPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
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

  const handleSignOut = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    router.push('/sign-in');
  };

  // [Task]: T055 - WebSocket real-time sync
  // Trigger refresh when task events occur from other tabs/users
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const triggerRefresh = useCallback(() => {
    setRefreshTrigger(prev => prev + 1);
  }, []);

  const { isConnected } = useTaskWebSocket(token, {
    onTaskCreated: triggerRefresh,
    onTaskUpdated: triggerRefresh,
    onTaskCompleted: triggerRefresh,
    onTaskDeleted: triggerRefresh,
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

  // Loading state
  if (!user || !token) {
    return (
      <div
        style={{
          minHeight: '100vh',
          backgroundColor: '#f0f2f5',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <div
          style={{
            width: '40px',
            height: '40px',
            border: '4px solid #e7f3ff',
            borderTopColor: '#1877f2',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
          }}
        />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
      {/* Header */}
      <header
        style={{
          backgroundColor: '#1877f2',
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
          position: 'sticky',
          top: 0,
          zIndex: 100,
        }}
      >
        <div
          style={{
            maxWidth: '960px',
            margin: '0 auto',
            padding: '0 16px',
            height: '56px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <Link
            href="/"
            style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#ffffff',
              textDecoration: 'none',
            }}
          >
            Todo App
          </Link>

          {/* Navigation */}
          <nav
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <Link
              href="/todos"
              style={{
                padding: '8px 16px',
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                color: '#ffffff',
                borderRadius: '6px',
                textDecoration: 'none',
                fontSize: '14px',
                fontWeight: '500',
              }}
            >
              Todo List
            </Link>
            <Link
              href="/chat"
              style={{
                padding: '8px 16px',
                backgroundColor: '#ffffff',
                color: '#1877f2',
                borderRadius: '6px',
                textDecoration: 'none',
                fontSize: '14px',
                fontWeight: '600',
              }}
            >
              AI Chat
            </Link>
          </nav>

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
                color: '#1877f2',
              }}
            >
              {user?.name?.[0]?.toUpperCase() || 'U'}
            </button>

            {showUserMenu && (
              <div
                style={{
                  position: 'absolute',
                  top: '100%',
                  right: 0,
                  marginTop: '8px',
                  backgroundColor: '#ffffff',
                  borderRadius: '8px',
                  boxShadow: '0 2px 12px rgba(0, 0, 0, 0.15)',
                  minWidth: '200px',
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    padding: '12px 16px',
                    borderBottom: '1px solid #e4e6eb',
                  }}
                >
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
                    color: '#1c1e21',
                  }}
                >
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main
        style={{
          maxWidth: '800px',
          margin: '0 auto',
          padding: '24px 16px',
          height: 'calc(100vh - 104px)', // Account for header and padding
        }}
      >
        <ChatWindow token={token} />
      </main>
    </div>
  );
}
