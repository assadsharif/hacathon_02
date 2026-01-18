#!/usr/bin/env python3
"""
Test script to verify FastAPI backend setup.

This script checks:
1. All modules can be imported
2. FastAPI app can be initialized
3. Database connection can be established
4. All routes are registered

Run with: python test_setup.py
"""

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import main
        import database
        import models
        import schemas
        from routers import todos
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_app_initialization():
    """Test that FastAPI app can be initialized"""
    print("\nTesting FastAPI app initialization...")
    try:
        from main import app
        print(f"✅ FastAPI app created: {app.title}")
        print(f"   Version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ App initialization failed: {e}")
        return False


def test_database_connection():
    """Test database connectivity"""
    print("\nTesting database connection...")
    try:
        from database import check_database_connection
        is_connected = check_database_connection()
        if is_connected:
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False


def test_routes():
    """Test that routes are properly configured"""
    print("\nTesting routes...")
    try:
        from main import app
        routes = [route.path for route in app.routes]
        print(f"✅ Registered routes:")
        for route in routes:
            print(f"   - {route}")
        return True
    except Exception as e:
        print(f"❌ Routes test error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("FastAPI Backend Setup Test")
    print("=" * 60)

    results = []
    results.append(("Imports", test_imports()))
    results.append(("App Initialization", test_app_initialization()))
    results.append(("Database Connection", test_database_connection()))
    results.append(("Routes", test_routes()))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed! Backend setup is complete.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start server: uvicorn main:app --reload --port 8000")
        print("3. Visit API docs: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit(main())
