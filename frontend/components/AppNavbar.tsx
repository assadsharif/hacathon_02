/**
 * AppNavbar - Shared navigation bar for authenticated pages
 * Provides navigation between Todos and Chat interfaces
 */

'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AppNavbarProps {
  user: User | null;
  onSignOut: () => void;
  showSearch?: boolean;
  searchQuery?: string;
  onSearchChange?: (query: string) => void;
}

export function AppNavbar({
  user,
  onSignOut,
  showSearch = false,
  searchQuery = '',
  onSearchChange
}: AppNavbarProps) {
  const pathname = usePathname();
  const [showUserMenu, setShowUserMenu] = useState(false);

  const isActive = (path: string) => pathname === path;

  return (
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
        {/* Logo */}
        <Link href="/" style={{
          fontSize: '24px',
          fontWeight: 'bold',
          color: '#ffffff',
          textDecoration: 'none'
        }}>
          Todo App
        </Link>

        {/* Navigation Links */}
        <nav style={{
          display: 'flex',
          gap: '8px',
          alignItems: 'center'
        }}>
          <Link
            href="/todos"
            style={{
              padding: '8px 16px',
              borderRadius: '6px',
              color: '#ffffff',
              textDecoration: 'none',
              fontWeight: '600',
              fontSize: '15px',
              backgroundColor: isActive('/todos') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
              transition: 'background-color 0.2s'
            }}
          >
            📝 Todos
          </Link>
          <Link
            href="/chat"
            style={{
              padding: '8px 16px',
              borderRadius: '6px',
              color: '#ffffff',
              textDecoration: 'none',
              fontWeight: '600',
              fontSize: '15px',
              backgroundColor: isActive('/chat') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
              transition: 'background-color 0.2s'
            }}
          >
            💬 AI Chat
          </Link>
        </nav>

        {/* Search Bar (optional) */}
        {showSearch && onSearchChange && (
          <div style={{
            flex: 1,
            maxWidth: '400px',
            margin: '0 20px'
          }}>
            <input
              type="text"
              placeholder="Search todos..."
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
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
        )}

        {/* User Menu */}
        <div style={{ position: 'relative' }}>
          <button
            onClick={() => setShowUserMenu(!showUserMenu)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '4px 12px 4px 4px',
              borderRadius: '20px',
              backgroundColor: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              cursor: 'pointer',
              color: '#ffffff'
            }}
          >
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              backgroundColor: '#ffffff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#1877f2',
              fontWeight: 'bold',
              fontSize: '14px'
            }}>
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <span style={{ fontSize: '14px', fontWeight: '600' }}>
              {user?.name || 'User'}
            </span>
            <span style={{ fontSize: '12px' }}>▼</span>
          </button>

          {/* Dropdown Menu */}
          {showUserMenu && (
            <>
              {/* Backdrop */}
              <div
                onClick={() => setShowUserMenu(false)}
                style={{
                  position: 'fixed',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  zIndex: 999
                }}
              />

              {/* Menu */}
              <div style={{
                position: 'absolute',
                top: '100%',
                right: 0,
                marginTop: '8px',
                backgroundColor: '#ffffff',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                minWidth: '200px',
                overflow: 'hidden',
                zIndex: 1000
              }}>
                <div style={{
                  padding: '12px 16px',
                  borderBottom: '1px solid #e4e6eb'
                }}>
                  <div style={{ fontWeight: '600', fontSize: '15px', color: '#1c1e21' }}>
                    {user?.name}
                  </div>
                  <div style={{ fontSize: '13px', color: '#65676b' }}>
                    {user?.email}
                  </div>
                </div>

                <button
                  onClick={() => {
                    setShowUserMenu(false);
                    onSignOut();
                  }}
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    border: 'none',
                    backgroundColor: 'transparent',
                    textAlign: 'left',
                    cursor: 'pointer',
                    fontSize: '15px',
                    color: '#1c1e21',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#f0f2f5';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent';
                  }}
                >
                  🚪 Sign Out
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
