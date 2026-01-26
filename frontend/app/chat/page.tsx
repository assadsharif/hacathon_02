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
import { AppNavbar } from '@/components/AppNavbar';
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
      {/* Navigation Bar */}
      <AppNavbar
        user={user}
        onSignOut={handleSignOut}
      />

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
