'use client';

import "./globals.css";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const pathname = usePathname();
  const router = useRouter();
  const { data: session, isPending } = useSession();

  const isAuthPage = pathname === '/sign-in' || pathname === '/sign-up';

  const handleSignOut = async () => {
    await signOut();
    router.push('/');
  };

  return (
    <html lang="en">
      <head>
        <title>Todo App - Phase II</title>
        <meta name="description" content="Full-stack todo application with Next.js and FastAPI" />
      </head>
      <body className="antialiased">
        <style jsx global>{`
          @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

          .header-glass {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px) saturate(180%);
            border-bottom: 1px solid rgba(229, 231, 235, 0.5);
          }

          .nav-link {
            transition: all 0.2s ease;
          }

          .nav-link:hover {
            transform: translateY(-1px);
          }
        `}</style>

        <div className="min-h-screen bg-gray-50">
          {!isAuthPage && (
            <header className="header-glass sticky top-0 z-50 shadow-sm">
              <div className="max-w-7xl mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                  {/* Logo & Brand */}
                  <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-pink-500 flex items-center justify-center shadow-md">
                      <span className="text-xl font-bold text-white" style={{ fontFamily: 'Outfit, sans-serif' }}>
                        T
                      </span>
                    </div>
                    <div>
                      <h1 className="text-2xl font-bold text-gray-900" style={{ fontFamily: 'Outfit, sans-serif' }}>
                        Todo App
                      </h1>
                      <p className="text-xs text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                        Phase II
                      </p>
                    </div>
                  </Link>

                  {/* Navigation */}
                  <nav className="flex items-center gap-2">
                    {isPending ? (
                      <div className="w-8 h-8 animate-spin rounded-full border-2 border-purple-500 border-t-transparent"></div>
                    ) : session ? (
                      <>
                        {/* Authenticated Navigation */}
                        <Link
                          href="/todos"
                          className={`nav-link px-4 py-2 rounded-lg font-medium transition-all ${
                            pathname.startsWith('/todos')
                              ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white shadow-md'
                              : 'text-gray-700 hover:bg-gray-100'
                          }`}
                          style={{ fontFamily: 'DM Sans, sans-serif' }}
                        >
                          My Todos
                        </Link>
                        <Link
                          href="/todos/new"
                          className="nav-link px-4 py-2 rounded-lg font-medium text-gray-700 hover:bg-gray-100 transition-all inline-flex items-center gap-2"
                          style={{ fontFamily: 'DM Sans, sans-serif' }}
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                          </svg>
                          New
                        </Link>

                        {/* User Menu */}
                        <div className="ml-4 flex items-center gap-3 pl-4 border-l border-gray-300">
                          <div className="text-right hidden sm:block">
                            <p className="text-sm font-semibold text-gray-900" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                              {session.user.name || 'User'}
                            </p>
                            <p className="text-xs text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                              {session.user.email}
                            </p>
                          </div>
                          <button
                            onClick={handleSignOut}
                            className="nav-link px-4 py-2 rounded-lg font-medium text-gray-700 hover:bg-red-50 hover:text-red-600 transition-all inline-flex items-center gap-2"
                            style={{ fontFamily: 'DM Sans, sans-serif' }}
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                            </svg>
                            Sign Out
                          </button>
                        </div>
                      </>
                    ) : (
                      <>
                        {/* Unauthenticated Navigation */}
                        <Link
                          href="/sign-in"
                          className="nav-link px-5 py-2 rounded-lg font-semibold text-gray-700 hover:bg-gray-100 transition-all"
                          style={{ fontFamily: 'DM Sans, sans-serif' }}
                        >
                          Sign In
                        </Link>
                        <Link
                          href="/sign-up"
                          className="nav-link px-5 py-2 rounded-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-500 text-white shadow-md hover:shadow-lg transition-all"
                          style={{ fontFamily: 'DM Sans, sans-serif' }}
                        >
                          Sign Up
                        </Link>
                      </>
                    )}
                  </nav>
                </div>
              </div>
            </header>
          )}

          <main className={!isAuthPage ? "max-w-7xl mx-auto px-4 py-8" : ""}>
            {children}
          </main>

          {/* Footer */}
          {!isAuthPage && (
            <footer className="mt-16 border-t border-gray-200 bg-white/50 backdrop-blur-sm">
              <div className="max-w-7xl mx-auto px-4 py-8">
                <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                  <div className="text-center md:text-left">
                    <p className="text-sm text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                      © 2026 Todo App - Phase II Full-Stack Application
                    </p>
                    <p className="text-xs text-gray-500 mt-1" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                      Built with Next.js, FastAPI, and PostgreSQL
                    </p>
                  </div>
                  <div className="flex gap-6 text-sm text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                    <a
                      href="http://localhost:8000/docs"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-purple-600 transition-colors"
                    >
                      API Docs
                    </a>
                    <a
                      href="http://localhost:8000/health"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-purple-600 transition-colors"
                    >
                      Health Check
                    </a>
                  </div>
                </div>
              </div>
            </footer>
          )}
        </div>
      </body>
    </html>
  );
}
