/**
 * User Menu Component
 * [Task]: AUTH-C7
 * [From]: authentication.spec.md
 *
 * Displays current user information and sign-out button.
 * Shows user's email and name (if available).
 *
 * Usage:
 *   <UserMenu />
 */

'use client';

import { useSession } from '@/lib/auth-client';
import { SignOutButton } from './SignOutButton';

export function UserMenu() {
    const { data: session, isPending } = useSession();

    if (isPending) {
        return (
            <div className="flex items-center space-x-4">
                <div className="h-8 w-32 bg-gray-200 animate-pulse rounded"></div>
            </div>
        );
    }

    if (!session) {
        return null;
    }

    return (
        <div className="flex items-center space-x-4">
            {/* User Info */}
            <div className="text-sm">
                <p className="font-medium text-gray-900">
                    {session.user.name || 'User'}
                </p>
                <p className="text-gray-500">{session.user.email}</p>
            </div>

            {/* Sign-Out Button */}
            <SignOutButton variant="secondary" />
        </div>
    );
}
