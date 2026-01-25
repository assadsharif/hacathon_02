/**
 * Better Auth Configuration
 * [Task]: AUTH-C2
 * [From]: authentication.spec.md, plan.md Frontend Better Auth Setup
 *
 * This module configures Better Auth for user authentication with JWT tokens.
 * Better Auth handles user registration, sign-in, session management, and JWT issuance.
 *
 * Security Model:
 * - JWT tokens issued with HS256 algorithm
 * - Tokens contain user_id and email claims
 * - 7-day token expiration (Better Auth default)
 * - Database-backed session storage
 * - Password hashing with bcrypt/argon2
 */

import { betterAuth } from "better-auth";
import { mcp } from "better-auth/plugins";
import { Pool } from "pg";

/**
 * PostgreSQL connection pool for Better Auth.
 * Using pg Pool directly for better compatibility with Neon's connection pooler.
 */
const pool = new Pool({
    connectionString: process.env.DATABASE_URL!,
    ssl: {
        rejectUnauthorized: false, // Required for Neon
    },
});

/**
 * Better Auth instance for the application.
 *
 * Configuration:
 * - Database URL: Environment variable for session storage
 * - JWT Secret: Shared with backend for token verification
 * - Email/Password: Default authentication provider
 * - MCP Plugin: Configures login page at /sign-in
 *
 * Usage:
 *   // In API routes or server components
 *   import { auth } from "@/lib/auth";
 *   const session = await auth.api.getSession({ headers: request.headers });
 */
export const auth = betterAuth({
    /**
     * Database configuration for session storage.
     * Better Auth requires a database to store user accounts and sessions.
     * Using pg Pool for better Neon compatibility.
     */
    database: pool,

    /**
     * JWT secret for token signing.
     * MUST match the JWT_SECRET in the backend .env file.
     *
     * CRITICAL: This secret is used to sign JWT tokens.
     * The backend verifies these tokens with the same secret.
     */
    secret: process.env.JWT_SECRET || process.env.BETTER_AUTH_SECRET || "fallback-secret-for-dev",

    /**
     * Email and password authentication provider.
     * This is the default authentication method for the application.
     */
    emailAndPassword: {
        enabled: true,
        /**
         * Require email verification before allowing login.
         * Set to false for development, true for production.
         */
        requireEmailVerification: false,
    },

    /**
     * MCP (Model Context Protocol) plugin configuration.
     * This plugin provides a standardized login page.
     */
    plugins: [
        mcp({
            /**
             * Login page URL.
             * Users will be redirected here when authentication is required.
             */
            loginPage: "/sign-in",
        }),
    ],

    /**
     * Session configuration.
     * Better Auth manages sessions with JWT tokens.
     */
    session: {
        /**
         * Session expiration in seconds (7 days).
         * After this time, users must sign in again.
         */
        expiresIn: 60 * 60 * 24 * 7, // 7 days
    },
});

/**
 * Type definitions for Better Auth session.
 * Use these types in your components and API routes.
 *
 * Example:
 *   const session = await auth.api.getSession({ headers });
 *   if (session) {
 *     const userId: string = session.user.id;
 *     const email: string = session.user.email;
 *   }
 */
export type Session = Awaited<ReturnType<typeof auth.api.getSession>>;
export type User = Session extends { user: infer U } ? U : never;
