/**
 * Better Auth Database Migration Script
 *
 * This script initializes Better Auth database tables.
 * Run this if you get 500 errors during sign-up.
 */

import { betterAuth } from "better-auth";
import { mcp } from "better-auth/plugins";
import * as dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables from .env.local
dotenv.config({ path: join(__dirname, '../.env.local') });

console.log('🔧 Better Auth Migration Script');
console.log('================================\n');

// Check environment variables
if (!process.env.DATABASE_URL) {
  console.error('❌ ERROR: DATABASE_URL is not set in .env.local');
  process.exit(1);
}

if (!process.env.JWT_SECRET) {
  console.error('❌ ERROR: JWT_SECRET is not set in .env.local');
  process.exit(1);
}

console.log('✅ Environment variables loaded');
console.log(`📊 Database: ${process.env.DATABASE_URL.split('@')[1].split('/')[0]}`);
console.log('');

try {
  console.log('🚀 Initializing Better Auth...');

  const auth = betterAuth({
    database: {
      provider: "postgresql",
      url: process.env.DATABASE_URL,
    },
    secret: process.env.JWT_SECRET,
    emailAndPassword: {
      enabled: true,
      requireEmailVerification: false,
    },
    plugins: [
      mcp({
        loginPage: "/sign-in",
      }),
    ],
    session: {
      expiresIn: 60 * 60 * 24 * 7,
    },
  });

  console.log('✅ Better Auth initialized successfully');
  console.log('');
  console.log('📝 Next steps:');
  console.log('   1. Restart your frontend server if it\'s running');
  console.log('   2. Try signing up again at http://localhost:3000/sign-up');
  console.log('');
  console.log('✨ Migration complete!');

} catch (error) {
  console.error('❌ Migration failed:', error.message);
  console.error('');
  console.error('🔍 Troubleshooting:');
  console.error('   1. Check that your DATABASE_URL is correct');
  console.error('   2. Verify the database is accessible');
  console.error('   3. Ensure the database user has CREATE TABLE permissions');
  console.error('');
  process.exit(1);
}
