/**
 * Test endpoint to verify environment variables
 */
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    hasDatabaseUrl: !!process.env.DATABASE_URL,
    hasJwtSecret: !!process.env.JWT_SECRET,
    databaseUrlPrefix: process.env.DATABASE_URL?.substring(0, 20) || 'not set',
    nodeEnv: process.env.NODE_ENV,
  });
}
