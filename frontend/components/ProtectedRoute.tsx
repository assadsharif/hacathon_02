/**
 * Protected Route Component
 * [Task]: AUTH-C6
 * [From]: authentication.spec.md
 *
 * Client-side wrapper for protected content.
 * Shows loading state while checking authentication,
 * redirects to sign-in if not authenticated.
 *
 * Usage:
 *   <ProtectedRoute>
 *     <TodoList />
 *   </ProtectedRoute>
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from '@/lib/auth-client';

interface ProtectedRouteProps {
    children: React.ReactNode;
    fallback?: React.ReactNode;
}

export function ProtectedRoute({ children, fallback }: ProtectedRouteProps) {
    const router = useRouter();
    const { data: session, isPending } = useSession();

    useEffect(() => {
        // If not loading and no session, redirect to sign-in
        if (!isPending && !session) {
            router.push('/sign-in');
        }
    }, [session, isPending, router]);

    // Show loading state while checking authentication
    if (isPending) {
        return (
            fallback || (
                <div className="min-h-screen flex items-center justify-center">
                    <div className="text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-600">Loading...</p>
                    </div>
                </div>
            )
        );
    }

    // If no session, show nothing (redirect will happen in useEffect)
    if (!session) {
        return null;
    }

    // Session exists, render protected content
    return <>{children}</>;
}
