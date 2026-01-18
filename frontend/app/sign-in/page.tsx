/**
 * Sign-In Page
 * [Task]: AUTH-C4
 * [From]: authentication.spec.md FR-AUTH-004 (User Sign In)
 *
 * This page allows existing users to sign in with email and password.
 * After successful authentication, users receive a JWT token and are redirected to the home page.
 *
 * User Story:
 * As a registered user, I want to sign in with my email and password
 * so that I can access my personal todo list.
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { signIn } from '@/lib/auth-client';

export default function SignInPage() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            // Call Better Auth sign-in
            const result = await signIn.email({
                email,
                password,
            });

            if (result.error) {
                // Display error message
                setError(result.error.message || 'Invalid email or password.');
                setIsLoading(false);
            } else {
                // Sign-in successful - redirect to home page
                router.push('/');
                router.refresh(); // Refresh to update session state
            }
        } catch (err) {
            setError('An unexpected error occurred. Please try again.');
            setIsLoading(false);
            console.error('Sign in error:', err);
        }
    };

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

                @keyframes float-in {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                @keyframes scale-in {
                    from {
                        opacity: 0;
                        transform: scale(0.95);
                    }
                    to {
                        opacity: 1;
                        transform: scale(1);
                    }
                }

                .animate-float-in {
                    animation: float-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                }

                .animate-scale-in {
                    animation: scale-in 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                }

                .gradient-bg {
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

                .glass-card {
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(20px) saturate(180%);
                    border: 1px solid rgba(255, 255, 255, 0.4);
                    box-shadow:
                        0 8px 32px rgba(0, 0, 0, 0.08),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
                }

                .input-field {
                    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                    border: 2px solid rgba(107, 70, 193, 0.15);
                    background: rgba(255, 255, 255, 0.7);
                }

                .input-field:focus {
                    outline: none;
                    border-color: #7B68EE;
                    background: rgba(255, 255, 255, 0.95);
                    box-shadow:
                        0 0 0 4px rgba(123, 104, 238, 0.1),
                        0 4px 12px rgba(123, 104, 238, 0.15);
                    transform: translateY(-1px);
                }

                .btn-primary {
                    background: linear-gradient(135deg, #7B68EE 0%, #C471ED 100%);
                    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                    box-shadow:
                        0 4px 16px rgba(123, 104, 238, 0.3),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
                }

                .btn-primary:hover:not(:disabled) {
                    transform: translateY(-2px);
                    box-shadow:
                        0 8px 24px rgba(123, 104, 238, 0.4),
                        0 0 0 1px rgba(255, 255, 255, 0.2) inset;
                }

                .btn-primary:active:not(:disabled) {
                    transform: translateY(0);
                }

                .btn-primary:disabled {
                    opacity: 0.7;
                    cursor: not-allowed;
                }

                .error-card {
                    background: linear-gradient(135deg, #FFF5F5 0%, #FFE5E5 100%);
                    border: 1px solid rgba(239, 68, 68, 0.2);
                    animation: float-in 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                }
            `}</style>

            <div className="gradient-bg min-h-screen flex items-center justify-center px-4 py-12 relative overflow-hidden">
                {/* Decorative elements */}
                <div className="absolute top-0 left-0 w-full h-full pointer-events-none overflow-hidden">
                    <div className="absolute top-[-10%] right-[-10%] w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
                    <div className="absolute bottom-[-10%] left-[-10%] w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
                </div>

                <div className="max-w-md w-full relative z-10">
                    {/* Logo/Brand */}
                    <div className="text-center mb-8 animate-float-in opacity-0" style={{ animationDelay: '0.1s' }}>
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white/90 backdrop-blur-sm shadow-lg mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                            <span className="text-3xl font-bold bg-gradient-to-br from-purple-600 to-pink-500 bg-clip-text text-transparent">T</span>
                        </div>
                        <h1 className="text-4xl font-bold text-white mb-2" style={{ fontFamily: 'Outfit, sans-serif', textShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
                            Welcome Back
                        </h1>
                        <p className="text-white/90 text-sm" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                            Sign in to continue managing your todos
                        </p>
                    </div>

                    {/* Main Card */}
                    <div className="glass-card rounded-3xl p-8 animate-scale-in opacity-0" style={{ animationDelay: '0.2s' }}>
                        {/* Header */}
                        <div className="text-center mb-8">
                            <h2 className="text-3xl font-bold text-gray-900 mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
                                Sign in to your account
                            </h2>
                            <p className="text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                                Please enter your details
                            </p>
                        </div>

                        {/* Sign-In Form */}
                        <form className="space-y-5" onSubmit={handleSubmit}>
                            {/* Error Message */}
                            {error && (
                                <div className="error-card rounded-xl p-4">
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

                            {/* Email Field */}
                            <div>
                                <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                                    Email address
                                </label>
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="input-field block w-full px-4 py-3 rounded-xl text-gray-900 placeholder-gray-400"
                                    placeholder="you@example.com"
                                    style={{ fontFamily: 'DM Sans, sans-serif' }}
                                />
                            </div>

                            {/* Password Field */}
                            <div>
                                <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                                    Password
                                </label>
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete="current-password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="input-field block w-full px-4 py-3 rounded-xl text-gray-900 placeholder-gray-400"
                                    placeholder="••••••••"
                                    style={{ fontFamily: 'DM Sans, sans-serif' }}
                                />
                            </div>

                            {/* Submit Button */}
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="btn-primary w-full py-3.5 px-6 rounded-xl text-white font-semibold text-base"
                                style={{ fontFamily: 'DM Sans, sans-serif' }}
                            >
                                {isLoading ? 'Signing in...' : 'Sign in'}
                            </button>

                            {/* Sign-Up Link */}
                            <div className="text-center pt-2">
                                <p className="text-sm text-gray-600" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                                    Don't have an account?{' '}
                                    <Link
                                        href="/sign-up"
                                        className="font-semibold text-transparent bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text hover:from-purple-700 hover:to-pink-600 transition-all"
                                    >
                                        Sign up
                                    </Link>
                                </p>
                            </div>
                        </form>
                    </div>

                    {/* Footer */}
                    <div className="text-center mt-6 animate-float-in opacity-0" style={{ animationDelay: '0.3s' }}>
                        <p className="text-white/70 text-sm" style={{ fontFamily: 'DM Sans, sans-serif' }}>
                            Secure authentication powered by Better Auth
                        </p>
                    </div>
                </div>
            </div>
        </>
    );
}
