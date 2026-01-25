/**
 * Better Auth Client for React Components
 * [Task]: AUTH-C2
 * [From]: authentication.spec.md
 *
 * This module provides React hooks and client-side utilities for authentication.
 * Use this in client components to access authentication state and actions.
 *
 * Usage in React components:
 *   'use client';
 *   import { useSession, signIn, signOut, signUp } from '@/lib/auth-client';
 *
 *   function MyComponent() {
 *     const { data: session, isPending } = useSession();
 *     if (isPending) return <div>Loading...</div>;
 *     if (!session) return <SignInButton />;
 *     return <div>Welcome {session.user.email}</div>;
 *   }
 */

import { createAuthClient } from "better-auth/react";

/**
 * Better Auth client for React components.
 *
 * This provides:
 * - useSession() hook for accessing current session
 * - signIn() function for email/password authentication
 * - signUp() function for user registration
 * - signOut() function for logging out
 */
export const {
    useSession,
    signIn,
    signUp,
    signOut,
} = createAuthClient({
    /**
     * Base URL for Better Auth API endpoints.
     * Better Auth creates API routes at /api/auth/*
     *
     * In development: http://localhost:3000
     * In production: Your deployed frontend URL
     */
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

/**
 * Sign in with email and password.
 *
 * @param email - User's email address
 * @param password - User's password
 * @returns Promise resolving to session data or error
 *
 * Example:
 *   const handleSignIn = async () => {
 *     const result = await signIn.email({
 *       email: 'user@example.com',
 *       password: 'password123'
 *     });
 *     if (result.error) {
 *       console.error('Sign in failed:', result.error);
 *     } else {
 *       console.log('Signed in:', result.data.user);
 *     }
 *   };
 */

/**
 * Sign up with email and password.
 *
 * @param email - User's email address
 * @param password - User's password
 * @param name - Optional user's display name
 * @returns Promise resolving to session data or error
 *
 * Example:
 *   const handleSignUp = async () => {
 *     const result = await signUp.email({
 *       email: 'newuser@example.com',
 *       password: 'securepassword',
 *       name: 'John Doe'
 *     });
 *     if (result.error) {
 *       console.error('Sign up failed:', result.error);
 *     } else {
 *       console.log('Account created:', result.data.user);
 *     }
 *   };
 */

/**
 * Sign out the current user.
 *
 * @returns Promise resolving when sign out is complete
 *
 * Example:
 *   const handleSignOut = async () => {
 *     await signOut();
 *     router.push('/sign-in');
 *   };
 */

/**
 * useSession hook for accessing authentication state.
 *
 * @returns Object containing session data and loading state
 *
 * Example:
 *   const { data: session, isPending, error } = useSession();
 *
 *   if (isPending) return <Spinner />;
 *   if (error) return <ErrorMessage error={error} />;
 *   if (!session) return <SignInPrompt />;
 *
 *   return <Dashboard user={session.user} />;
 */
