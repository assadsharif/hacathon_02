"""
Fix Database Schema
This script drops existing tables and recreates them with correct schema
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

print("🔧 Connecting to database...")
engine = create_engine(DATABASE_URL)

print("⚠️  WARNING: This will DROP existing tables!")
print("   - todos table will be dropped")
print("   - users table will be dropped")
print("")

try:
    with engine.connect() as conn:
        # Drop tables in correct order (todos first due to foreign key)
        print("🗑️  Dropping todos table...")
        conn.execute(text("DROP TABLE IF EXISTS todos CASCADE;"))
        conn.commit()
        print("✅ Dropped todos table")

        print("🗑️  Dropping users table...")
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        conn.commit()
        print("✅ Dropped users table")

        print("")
        print("✅ Database cleaned successfully!")
        print("")
        print("📝 Next steps:")
        print("   1. Start the backend server: ./start-backend.sh")
        print("   2. Tables will be auto-created with correct schema")

except Exception as e:
    print(f"❌ Error: {e}")
    raise
