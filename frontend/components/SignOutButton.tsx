/**
 * Sign-Out Button Component
 * [Task]: AUTH-C7
 * [From]: authentication.spec.md FR-AUTH-007 (User Sign Out)
 *
 * Provides a button to sign out the current user.
 * After signing out, redirects to the sign-in page.
 *
 * User Story:
 * As an authenticated user, I want to sign out of my account
 * so that my session is ended and my data is protected.
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signOut } from '@/lib/auth-client';

interface SignOutButtonProps {
    variant?: 'primary' | 'secondary' | 'text';
    className?: string;
}

export function SignOutButton({ variant = 'secondary', className = '' }: SignOutButtonProps) {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);

    const handleSignOut = async () => {
        setIsLoading(true);
        try {
            // Call Better Auth sign-out
            await signOut();

            // Redirect to sign-in page
            router.push('/sign-in');
            router.refresh(); // Refresh to clear session state
        } catch (error) {
            console.error('Sign out error:', error);
            // Even if error occurs, try to redirect
            router.push('/sign-in');
        } finally {
            setIsLoading(false);
        }
    };

    // Button styles based on variant
    const variantStyles = {
        primary: 'bg-blue-600 hover:bg-blue-700 text-white',
        secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-900',
        text: 'bg-transparent hover:bg-gray-100 text-gray-700',
    };

    return (
        <button
            onClick={handleSignOut}
            disabled={isLoading}
            className={`
                px-4 py-2 rounded-md font-medium
                focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                disabled:opacity-50 disabled:cursor-not-allowed
                transition-colors
                ${variantStyles[variant]}
                ${className}
            `}
        >
            {isLoading ? 'Signing out...' : 'Sign out'}
        </button>
    );
}
