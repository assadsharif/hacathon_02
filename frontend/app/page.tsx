'use client';

import Link from "next/link";

export default function Home() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f3f4f6' }}>
      {/* Header */}
      <header style={{
        backgroundColor: '#ffffff',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        padding: '12px 0'
      }}>
        <div style={{
          maxWidth: '980px',
          margin: '0 auto',
          padding: '0 16px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#3b82f6' }}>
            Todo App
          </h1>
          <div style={{ display: 'flex', gap: '12px' }}>
            <Link href="/sign-in" style={{
              padding: '8px 16px',
              fontSize: '15px',
              fontWeight: '600',
              color: '#3b82f6',
              textDecoration: 'none',
              borderRadius: '6px',
              backgroundColor: '#dbeafe'
            }}>
              Log In
            </Link>
            <Link href="/sign-up" style={{
              padding: '8px 16px',
              fontSize: '15px',
              fontWeight: '600',
              color: '#ffffff',
              textDecoration: 'none',
              borderRadius: '6px',
              backgroundColor: '#3b82f6'
            }}>
              Sign Up
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main style={{ maxWidth: '980px', margin: '0 auto', padding: '60px 16px' }}>
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
          <h2 style={{
            fontSize: '48px',
            fontWeight: 'bold',
            color: '#1f2937',
            marginBottom: '16px',
            lineHeight: '1.2'
          }}>
            Manage your tasks
            <br />
            <span style={{ color: '#3b82f6' }}>simply and efficiently</span>
          </h2>
          <p style={{
            fontSize: '20px',
            color: '#6b7280',
            marginBottom: '32px',
            maxWidth: '600px',
            margin: '0 auto 32px'
          }}>
            A clean, fast todo application with AI-powered chat to help you stay organized and productive. Manage tasks naturally with conversational AI.
          </p>
          <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link href="/sign-up" style={{
              padding: '14px 32px',
              fontSize: '18px',
              fontWeight: 'bold',
              color: '#ffffff',
              textDecoration: 'none',
              borderRadius: '6px',
              backgroundColor: '#3b82f6',
              transition: 'background-color 0.2s'
            }}>
              Get Started Free
            </Link>
            <Link href="/chat" style={{
              padding: '14px 32px',
              fontSize: '18px',
              fontWeight: '600',
              color: '#ffffff',
              textDecoration: 'none',
              borderRadius: '6px',
              backgroundColor: '#8b5cf6',
              transition: 'background-color 0.2s'
            }}>
              💬 Try AI Chat
            </Link>
            <Link href="/todos" style={{
              padding: '14px 32px',
              fontSize: '18px',
              fontWeight: '600',
              color: '#1f2937',
              textDecoration: 'none',
              borderRadius: '6px',
              backgroundColor: '#ffffff',
              border: '1px solid #e5e7eb'
            }}>
              View Todos
            </Link>
          </div>
        </div>

        {/* Features */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '24px',
          marginBottom: '60px'
        }}>
          {/* Feature 1 */}
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '24px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e5e7eb'
          }}>
            <div style={{
              width: '48px',
              height: '48px',
              backgroundColor: '#dbeafe',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '16px',
              fontSize: '24px'
            }}>
              ➕
            </div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1f2937', marginBottom: '8px' }}>
              Create Tasks
            </h3>
            <p style={{ fontSize: '15px', color: '#6b7280' }}>
              Quickly add new tasks with titles and descriptions. Stay on top of what needs to be done.
            </p>
          </div>

          {/* Feature 2 */}
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '24px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e5e7eb'
          }}>
            <div style={{
              width: '48px',
              height: '48px',
              backgroundColor: '#d1fae5',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '16px',
              fontSize: '24px'
            }}>
              ✓
            </div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1f2937', marginBottom: '8px' }}>
              Mark Complete
            </h3>
            <p style={{ fontSize: '15px', color: '#6b7280' }}>
              Check off tasks as you complete them. Track your progress throughout the day.
            </p>
          </div>

          {/* Feature 3 - AI Chat */}
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '24px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e5e7eb'
          }}>
            <div style={{
              width: '48px',
              height: '48px',
              backgroundColor: '#ede9fe',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '16px',
              fontSize: '24px'
            }}>
              💬
            </div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1f2937', marginBottom: '8px' }}>
              AI Chat Assistant
            </h3>
            <p style={{ fontSize: '15px', color: '#6b7280' }}>
              Manage todos with natural language. Just chat with our AI to create, update, and organize tasks.
            </p>
          </div>

          {/* Feature 4 */}
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '8px',
            padding: '24px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e5e7eb'
          }}>
            <div style={{
              width: '48px',
              height: '48px',
              backgroundColor: '#f3f4f6',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '16px',
              fontSize: '24px'
            }}>
              🔍
            </div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1f2937', marginBottom: '8px' }}>
              Filter & Search
            </h3>
            <p style={{ fontSize: '15px', color: '#6b7280' }}>
              Find tasks quickly with search and filters. Focus on what matters most.
            </p>
          </div>
        </div>

        {/* Tech Stack */}
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '8px',
          padding: '32px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          textAlign: 'center',
          border: '1px solid #e5e7eb'
        }}>
          <h3 style={{ fontSize: '24px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>
            Built with Modern Technology
          </h3>
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '12px',
            justifyContent: 'center'
          }}>
            {['Next.js', 'FastAPI', 'PostgreSQL', 'AI Chat', 'TypeScript'].map((tech) => (
              <span key={tech} style={{
                padding: '8px 16px',
                backgroundColor: '#f3f4f6',
                borderRadius: '20px',
                fontSize: '14px',
                color: '#6b7280',
                fontWeight: '500'
              }}>
                {tech}
              </span>
            ))}
          </div>
          <div style={{ marginTop: '24px' }}>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#3b82f6', textDecoration: 'none', fontSize: '15px', fontWeight: '600' }}
            >
              View API Documentation →
            </a>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer style={{
        backgroundColor: '#ffffff',
        borderTop: '1px solid #e5e7eb',
        padding: '24px 0',
        marginTop: '60px'
      }}>
        <div style={{
          maxWidth: '980px',
          margin: '0 auto',
          padding: '0 16px',
          textAlign: 'center',
          color: '#6b7280',
          fontSize: '14px'
        }}>
          <p>Todo App - Full-Stack Application with AI Chat</p>
        </div>
      </footer>
    </div>
  );
}
