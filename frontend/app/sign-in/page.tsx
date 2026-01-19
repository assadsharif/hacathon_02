'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
            const response = await fetch(`${API_URL}/api/auth/sign-in`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.detail || 'Invalid email or password.');
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
            backgroundColor: '#f0f2f5',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px'
        }}>
            <div style={{ width: '100%', maxWidth: '396px' }}>
                {/* Logo */}
                <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                    <h1 style={{
                        fontSize: '42px',
                        fontWeight: 'bold',
                        color: '#1877f2',
                        marginBottom: '10px'
                    }}>
                        Todo App
                    </h1>
                    <p style={{ fontSize: '16px', color: '#606770' }}>
                        Manage your tasks efficiently
                    </p>
                </div>

                {/* Login Card */}
                <div style={{
                    backgroundColor: '#ffffff',
                    borderRadius: '8px',
                    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1)',
                    padding: '20px'
                }}>
                    <form onSubmit={handleSubmit}>
                        {error && (
                            <div style={{
                                backgroundColor: '#ffebe8',
                                border: '1px solid #dd3c10',
                                borderRadius: '4px',
                                padding: '12px',
                                marginBottom: '16px',
                                color: '#dd3c10',
                                fontSize: '14px'
                            }}>
                                {error}
                            </div>
                        )}

                        <input
                            type="email"
                            placeholder="Email address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            style={{
                                width: '100%',
                                padding: '14px 16px',
                                fontSize: '17px',
                                border: '1px solid #dddfe2',
                                borderRadius: '6px',
                                marginBottom: '12px',
                                outline: 'none',
                                backgroundColor: '#fff',
                                color: '#1c1e21'
                            }}
                        />

                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            style={{
                                width: '100%',
                                padding: '14px 16px',
                                fontSize: '17px',
                                border: '1px solid #dddfe2',
                                borderRadius: '6px',
                                marginBottom: '12px',
                                outline: 'none',
                                backgroundColor: '#fff',
                                color: '#1c1e21'
                            }}
                        />

                        <button
                            type="submit"
                            disabled={isLoading}
                            style={{
                                width: '100%',
                                padding: '14px 16px',
                                fontSize: '20px',
                                fontWeight: 'bold',
                                backgroundColor: '#1877f2',
                                color: '#ffffff',
                                border: 'none',
                                borderRadius: '6px',
                                cursor: isLoading ? 'not-allowed' : 'pointer',
                                opacity: isLoading ? 0.7 : 1
                            }}
                        >
                            {isLoading ? 'Logging in...' : 'Log In'}
                        </button>

                        <div style={{ textAlign: 'center', marginTop: '16px' }}>
                            <Link href="#" style={{
                                color: '#1877f2',
                                fontSize: '14px',
                                textDecoration: 'none'
                            }}>
                                Forgotten password?
                            </Link>
                        </div>

                        <div style={{
                            borderTop: '1px solid #dadde1',
                            marginTop: '20px',
                            paddingTop: '20px',
                            textAlign: 'center'
                        }}>
                            <Link href="/sign-up" style={{
                                display: 'inline-block',
                                padding: '14px 24px',
                                fontSize: '17px',
                                fontWeight: 'bold',
                                backgroundColor: '#42b72a',
                                color: '#ffffff',
                                border: 'none',
                                borderRadius: '6px',
                                textDecoration: 'none'
                            }}>
                                Create new account
                            </Link>
                        </div>
                    </form>
                </div>

                <div style={{
                    textAlign: 'center',
                    marginTop: '28px',
                    fontSize: '14px',
                    color: '#737373'
                }}>
                    <p>Phase II - Todo Application</p>
                </div>
            </div>
        </div>
    );
}
