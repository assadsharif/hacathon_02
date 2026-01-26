'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function SignUpPage() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            const response = await fetch(`${API_URL}/api/auth/sign-up`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.detail || 'Sign up failed. Please try again.');
                setIsLoading(false);
                return;
            }

            // Store the token in localStorage
            localStorage.setItem('auth_token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));

            router.push('/todos');
            router.refresh();
        } catch (err) {
            setError('An unexpected error occurred. Please try again.');
            setIsLoading(false);
        }
    };

    return (
        <div style={{
            minHeight: '100vh',
            backgroundColor: '#f3f4f6',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px'
        }}>
            <div style={{ width: '100%', maxWidth: '432px' }}>
                {/* Logo */}
                <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                    <h1 style={{
                        fontSize: '42px',
                        fontWeight: 'bold',
                        color: '#3b82f6',
                        marginBottom: '10px'
                    }}>
                        Todo App
                    </h1>
                </div>

                {/* Sign Up Card */}
                <div style={{
                    backgroundColor: '#ffffff',
                    borderRadius: '8px',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1)',
                    padding: '20px'
                }}>
                    <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                        <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1f2937' }}>
                            Create a new account
                        </h2>
                        <p style={{ fontSize: '15px', color: '#6b7280', marginTop: '4px' }}>
                            It&apos;s quick and easy.
                        </p>
                    </div>

                    <div style={{ borderTop: '1px solid #e5e7eb', margin: '16px 0' }}></div>

                    <form onSubmit={handleSubmit}>
                        {error && (
                            <div style={{
                                backgroundColor: '#fee2e2',
                                border: '1px solid #ef4444',
                                borderRadius: '4px',
                                padding: '12px',
                                marginBottom: '16px',
                                color: '#ef4444',
                                fontSize: '14px'
                            }}>
                                {error}
                            </div>
                        )}

                        <input
                            type="text"
                            placeholder="Full name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                            style={{
                                width: '100%',
                                padding: '11px',
                                fontSize: '15px',
                                border: '1px solid #e5e7eb',
                                borderRadius: '5px',
                                marginBottom: '12px',
                                outline: 'none',
                                backgroundColor: '#f3f4f6',
                                color: '#1f2937'
                            }}
                        />

                        <input
                            type="email"
                            placeholder="Email address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            style={{
                                width: '100%',
                                padding: '11px',
                                fontSize: '15px',
                                border: '1px solid #e5e7eb',
                                borderRadius: '5px',
                                marginBottom: '12px',
                                outline: 'none',
                                backgroundColor: '#f3f4f6',
                                color: '#1f2937'
                            }}
                        />

                        <input
                            type="password"
                            placeholder="New password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            minLength={8}
                            style={{
                                width: '100%',
                                padding: '11px',
                                fontSize: '15px',
                                border: '1px solid #e5e7eb',
                                borderRadius: '5px',
                                marginBottom: '16px',
                                outline: 'none',
                                backgroundColor: '#f3f4f6',
                                color: '#1f2937'
                            }}
                        />

                        <p style={{ fontSize: '11px', color: '#6b7280', marginBottom: '16px' }}>
                            By clicking Sign Up, you agree to our Terms, Privacy Policy and Cookies Policy.
                        </p>

                        <div style={{ textAlign: 'center' }}>
                            <button
                                type="submit"
                                disabled={isLoading}
                                style={{
                                    padding: '10px 60px',
                                    fontSize: '18px',
                                    fontWeight: 'bold',
                                    backgroundColor: '#10b981',
                                    color: '#ffffff',
                                    border: 'none',
                                    borderRadius: '6px',
                                    cursor: isLoading ? 'not-allowed' : 'pointer',
                                    opacity: isLoading ? 0.7 : 1
                                }}
                            >
                                {isLoading ? 'Creating...' : 'Sign Up'}
                            </button>
                        </div>

                        <div style={{ textAlign: 'center', marginTop: '20px' }}>
                            <Link href="/sign-in" style={{
                                color: '#3b82f6',
                                fontSize: '17px',
                                textDecoration: 'none'
                            }}>
                                Already have an account?
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
