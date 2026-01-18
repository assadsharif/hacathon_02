'use client';

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <>
      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

        @keyframes gradient-shift {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }

        @keyframes float-in-up {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fade-in {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        .gradient-bg-home {
          background: linear-gradient(
            135deg,
            #FF6B6B 0%,
            #FF8E53 15%,
            #FE6B8B 30%,
            #C471ED 50%,
            #7B68EE 70%,
            #4A5FBF 100%
          );
          background-size: 400% 400%;
          animation: gradient-shift 15s ease infinite;
        }

        .glass-card-home {
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(20px) saturate(180%);
          border: 1px solid rgba(255, 255, 255, 0.4);
          box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.08),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        }

        .btn-gradient {
          background: linear-gradient(135deg, #7B68EE 0%, #C471ED 100%);
          transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
          box-shadow:
            0 4px 16px rgba(123, 104, 238, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        }

        .btn-gradient:hover {
          transform: translateY(-2px);
          box-shadow:
            0 8px 24px rgba(123, 104, 238, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset;
        }

        .btn-gradient:active {
          transform: translateY(0);
        }

        .btn-outline {
          background: rgba(255, 255, 255, 0.2);
          border: 2px solid rgba(255, 255, 255, 0.4);
          backdrop-filter: blur(10px);
          transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .btn-outline:hover {
          background: rgba(255, 255, 255, 0.3);
          border-color: rgba(255, 255, 255, 0.6);
          transform: translateY(-2px);
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }

        .feature-card {
          transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .feature-card:hover {
          transform: translateY(-4px);
          box-shadow:
            0 12px 40px rgba(0, 0, 0, 0.12),
            0 0 0 1px rgba(255, 255, 255, 0.15) inset;
        }

        .animate-in-1 {
          animation: float-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.1s forwards;
          opacity: 0;
        }

        .animate-in-2 {
          animation: float-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
          opacity: 0;
        }

        .animate-in-3 {
          animation: float-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards;
          opacity: 0;
        }

        .animate-in-4 {
          animation: float-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.4s forwards;
          opacity: 0;
        }
      `}</style>

      <div className="gradient-bg-home min-h-screen -mt-8 -mx-4 px-4 py-12 relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 left-0 w-full h-full pointer-events-none overflow-hidden">
          <div className="absolute top-[-10%] right-[-5%] w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-[-10%] left-[-5%] w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-white/5 rounded-full blur-3xl"></div>
        </div>

        <div className="max-w-4xl mx-auto relative z-10">
          {/* Hero Section */}
          <div className={`text-center mb-16 pt-12 ${mounted ? 'animate-in-1' : ''}`}>
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-white/90 backdrop-blur-sm shadow-2xl mb-6">
              <span className="text-4xl font-bold bg-gradient-to-br from-purple-600 to-pink-500 bg-clip-text text-transparent" style={{ fontFamily: 'Outfit, sans-serif' }}>
                T
              </span>
            </div>
            <h1 className="text-6xl md:text-7xl font-bold text-white mb-6 leading-tight" style={{ fontFamily: 'Outfit, sans-serif', textShadow: '0 2px 20px rgba(0,0,0,0.15)' }}>
              Todo App
            </h1>
            <p className="text-xl md:text-2xl text-white/90 mb-4 max-w-2xl mx-auto" style={{ fontFamily: 'DM Sans, sans-serif' }}>
              A beautiful, full-stack web application for managing your tasks
            </p>
            <p className="text-md text-white/70 mb-10" style={{ fontFamily: 'DM Sans, sans-serif' }}>
              Built with Next.js, FastAPI, and PostgreSQL
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                href="/todos"
                className="btn-gradient inline-flex items-center px-8 py-4 rounded-xl text-white font-semibold text-lg shadow-lg"
                style={{ fontFamily: 'DM Sans, sans-serif' }}
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                View Todos
              </Link>
              <Link
                href="/todos/new"
                className="btn-outline inline-flex items-center px-8 py-4 rounded-xl text-white font-semibold text-lg"
                style={{ fontFamily: 'DM Sans, sans-serif' }}
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Create Todo
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12 ${mounted ? 'animate-in-2' : ''}`}>
            {/* Architecture Card */}
            <div className="glass-card-home rounded-3xl p-8 feature-card">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center mb-4 shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Modern Stack
              </h3>
              <ul className="space-y-2 text-gray-700" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                <li className="flex items-start">
                  <span className="text-purple-500 mr-2 mt-1">✓</span>
                  <span>Next.js 16 with App Router</span>
                </li>
                <li className="flex items-start">
                  <span className="text-purple-500 mr-2 mt-1">✓</span>
                  <span>FastAPI Python Backend</span>
                </li>
                <li className="flex items-start">
                  <span className="text-purple-500 mr-2 mt-1">✓</span>
                  <span>PostgreSQL with SQLModel</span>
                </li>
                <li className="flex items-start">
                  <span className="text-purple-500 mr-2 mt-1">✓</span>
                  <span>TypeScript & Tailwind CSS</span>
                </li>
              </ul>
            </div>

            {/* Features Card */}
            <div className="glass-card-home rounded-3xl p-8 feature-card">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center mb-4 shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Rich Features
              </h3>
              <ul className="space-y-2 text-gray-700" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2 mt-1">✓</span>
                  <span>Create & manage tasks</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2 mt-1">✓</span>
                  <span>Mark todos as complete</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2 mt-1">✓</span>
                  <span>Search & filter todos</span>
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2 mt-1">✓</span>
                  <span>Sort by multiple criteria</span>
                </li>
              </ul>
            </div>

            {/* API Card */}
            <div className="glass-card-home rounded-3xl p-8 feature-card">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-teal-500 flex items-center justify-center mb-4 shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3" style={{ fontFamily: 'Outfit, sans-serif' }}>
                RESTful API
              </h3>
              <p className="text-gray-700 mb-4" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                Powerful FastAPI backend with automatic documentation
              </p>
              <div className="space-y-2">
                <a
                  href="http://localhost:8000/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full px-4 py-2 bg-gradient-to-r from-green-500 to-teal-500 text-white rounded-lg hover:from-green-600 hover:to-teal-600 transition-all text-center font-medium shadow-md"
                  style={{ fontFamily: 'DM Sans, sans-serif' }}
                >
                  API Docs
                </a>
                <a
                  href="http://localhost:8000/health"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full px-4 py-2 bg-white/50 text-gray-800 rounded-lg hover:bg-white/70 transition-all text-center font-medium"
                  style={{ fontFamily: 'DM Sans, sans-serif' }}
                >
                  Health Check
                </a>
              </div>
            </div>
          </div>

          {/* Bottom CTA */}
          <div className={`glass-card-home rounded-3xl p-8 text-center ${mounted ? 'animate-in-3' : ''}`}>
            <h3 className="text-3xl font-bold text-gray-900 mb-3" style={{ fontFamily: 'Outfit, sans-serif' }}>
              Ready to get organized?
            </h3>
            <p className="text-gray-700 mb-6 max-w-2xl mx-auto" style={{ fontFamily: 'DM Sans, sans-serif' }}>
              Start managing your tasks efficiently with our beautiful and intuitive todo application.
              Sign up now to create your first todo list!
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/sign-up"
                className="btn-gradient inline-flex items-center justify-center px-8 py-3 rounded-xl text-white font-semibold"
                style={{ fontFamily: 'DM Sans, sans-serif' }}
              >
                Get Started
              </Link>
              <Link
                href="/sign-in"
                className="inline-flex items-center justify-center px-8 py-3 rounded-xl text-gray-800 font-semibold bg-white/50 hover:bg-white/70 transition-all"
                style={{ fontFamily: 'DM Sans, sans-serif' }}
              >
                Sign In
              </Link>
            </div>
          </div>

          {/* Footer */}
          <div className={`text-center mt-12 ${mounted ? 'animate-in-4' : ''}`}>
            <p className="text-white/70 text-sm" style={{ fontFamily: 'DM Sans, sans-serif' }}>
              Phase II - Full-Stack Web Application
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
