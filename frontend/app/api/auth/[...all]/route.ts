/**
 * Better Auth API Route Handler
 * [Task]: AUTH-C2
 * [From]: authentication.spec.md
 *
 * This is a catch-all API route that handles all Better Auth requests.
 * Better Auth automatically creates endpoints for:
 * - POST /api/auth/sign-up - User registration
 * - POST /api/auth/sign-in/email - Email/password sign in
 * - POST /api/auth/sign-out - Sign out
 * - GET /api/auth/session - Get current session
 * - And other authentication-related endpoints
 *
 * This route delegates all authentication logic to Better Auth.
 */

// Force Node.js runtime (not Edge) for Better Auth compatibility
export const runtime = 'nodejs';

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

/**
 * Export Better Auth handlers for Next.js App Router.
 *
 * Better Auth automatically handles:
 * - Request validation
 * - Password hashing
 * - JWT token generation
 * - Session management
 * - Database operations
 *
 * All authentication endpoints are available at /api/auth/*
 */
export const { GET, POST } = toNextJsHandler(auth);
