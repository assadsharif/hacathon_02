#!/usr/bin/env python3
"""
Test CRUD Endpoints

This script tests all Todo CRUD endpoints to verify they work correctly.
It performs a full cycle: Create → Read → Update → Delete

Prerequisites:
- Backend server must be running (uvicorn main:app --reload --port 8000)
- Database must be accessible

Run with: python test_crud_endpoints.py
"""

import requests
import json
from typing import Optional

# API base URL
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/todos"


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_response(response: requests.Response):
    """Print response details"""
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def test_health_check():
    """Test health endpoints"""
    print_section("Health Check")

    # Test root endpoint
    print("\n1. Testing root endpoint (GET /)")
    response = requests.get(BASE_URL)
    print_response(response)

    # Test health endpoint
    print("\n2. Testing health endpoint (GET /health)")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)

    # Test database health
    print("\n3. Testing database health (GET /health/db)")
    response = requests.get(f"{BASE_URL}/health/db")
    print_response(response)

    return response.status_code == 200


def test_create_todo() -> Optional[int]:
    """Test creating a new todo"""
    print_section("CREATE Todo (POST /api/todos)")

    # Test case 1: Create active todo
    print("\n1. Creating active todo...")
    todo_data = {
        "title": "Test Todo - Phase II Backend",
        "status": "active"
    }
    response = requests.post(API_URL, json=todo_data)
    print_response(response)

    if response.status_code != 201:
        print("❌ Failed to create todo")
        return None

    todo_id = response.json()["id"]
    print(f"✅ Todo created with ID: {todo_id}")

    # Test case 2: Create completed todo
    print("\n2. Creating completed todo...")
    todo_data2 = {
        "title": "Another test todo",
        "status": "completed"
    }
    response = requests.post(API_URL, json=todo_data2)
    print_response(response)

    return todo_id


def test_list_todos():
    """Test listing todos"""
    print_section("LIST Todos (GET /api/todos)")

    # Test case 1: List all todos
    print("\n1. Listing all todos...")
    response = requests.get(API_URL)
    print_response(response)

    if response.status_code != 200:
        print("❌ Failed to list todos")
        return False

    todos = response.json()
    print(f"✅ Retrieved {len(todos)} todos")

    # Test case 2: Filter by status (active)
    print("\n2. Filtering active todos...")
    response = requests.get(API_URL, params={"status_filter": "active"})
    print_response(response)

    # Test case 3: Filter by status (completed)
    print("\n3. Filtering completed todos...")
    response = requests.get(API_URL, params={"status_filter": "completed"})
    print_response(response)

    return True


def test_get_todo(todo_id: int):
    """Test getting a single todo"""
    print_section(f"GET Todo by ID (GET /api/todos/{todo_id})")

    # Test case 1: Get existing todo
    print(f"\n1. Getting todo with ID {todo_id}...")
    response = requests.get(f"{API_URL}/{todo_id}")
    print_response(response)

    if response.status_code != 200:
        print("❌ Failed to get todo")
        return False

    print("✅ Todo retrieved successfully")

    # Test case 2: Get non-existent todo
    print("\n2. Trying to get non-existent todo (ID 99999)...")
    response = requests.get(f"{API_URL}/99999")
    print_response(response)

    if response.status_code == 404:
        print("✅ Correctly returned 404 for non-existent todo")

    return True


def test_update_todo(todo_id: int):
    """Test updating a todo"""
    print_section(f"UPDATE Todo (PUT /api/todos/{todo_id})")

    # Test case 1: Update status
    print(f"\n1. Updating status to 'completed'...")
    update_data = {
        "status": "completed"
    }
    response = requests.put(f"{API_URL}/{todo_id}", json=update_data)
    print_response(response)

    if response.status_code != 200:
        print("❌ Failed to update todo")
        return False

    print("✅ Status updated successfully")

    # Test case 2: Update title
    print(f"\n2. Updating title...")
    update_data = {
        "title": "Updated Todo Title - Phase II"
    }
    response = requests.put(f"{API_URL}/{todo_id}", json=update_data)
    print_response(response)

    # Test case 3: Update both fields
    print(f"\n3. Updating both title and status...")
    update_data = {
        "title": "Final Updated Title",
        "status": "active"
    }
    response = requests.put(f"{API_URL}/{todo_id}", json=update_data)
    print_response(response)

    # Test case 4: Update non-existent todo
    print("\n4. Trying to update non-existent todo (ID 99999)...")
    response = requests.put(f"{API_URL}/99999", json={"status": "completed"})
    print_response(response)

    if response.status_code == 404:
        print("✅ Correctly returned 404 for non-existent todo")

    return True


def test_delete_todo(todo_id: int):
    """Test deleting a todo"""
    print_section(f"DELETE Todo (DELETE /api/todos/{todo_id})")

    # Test case 1: Delete existing todo
    print(f"\n1. Deleting todo with ID {todo_id}...")
    response = requests.delete(f"{API_URL}/{todo_id}")
    print(f"Status Code: {response.status_code}")

    if response.status_code != 204:
        print("❌ Failed to delete todo")
        return False

    print("✅ Todo deleted successfully (204 No Content)")

    # Test case 2: Verify todo is deleted
    print(f"\n2. Verifying todo {todo_id} is deleted...")
    response = requests.get(f"{API_URL}/{todo_id}")
    print_response(response)

    if response.status_code == 404:
        print("✅ Confirmed todo is deleted")

    # Test case 3: Delete non-existent todo
    print("\n3. Trying to delete non-existent todo (ID 99999)...")
    response = requests.delete(f"{API_URL}/99999")
    print_response(response)

    if response.status_code == 404:
        print("✅ Correctly returned 404 for non-existent todo")

    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("  FastAPI CRUD Endpoints Test Suite")
    print("=" * 60)
    print(f"\nAPI URL: {API_URL}")
    print("Make sure the backend server is running:")
    print("  uvicorn main:app --reload --port 8000\n")

    results = []

    # Test health checks
    try:
        health_ok = test_health_check()
        results.append(("Health Checks", health_ok))
    except Exception as e:
        print(f"\n❌ Health check failed: {e}")
        print("\nIs the backend server running?")
        print("Start it with: uvicorn main:app --reload --port 8000")
        return 1

    # Test CREATE
    try:
        todo_id = test_create_todo()
        results.append(("CREATE", todo_id is not None))
    except Exception as e:
        print(f"\n❌ CREATE test failed: {e}")
        todo_id = None
        results.append(("CREATE", False))

    if todo_id is None:
        print("\n⚠️  Cannot continue tests without a valid todo ID")
        return 1

    # Test LIST
    try:
        list_ok = test_list_todos()
        results.append(("LIST", list_ok))
    except Exception as e:
        print(f"\n❌ LIST test failed: {e}")
        results.append(("LIST", False))

    # Test GET
    try:
        get_ok = test_get_todo(todo_id)
        results.append(("GET", get_ok))
    except Exception as e:
        print(f"\n❌ GET test failed: {e}")
        results.append(("GET", False))

    # Test UPDATE
    try:
        update_ok = test_update_todo(todo_id)
        results.append(("UPDATE", update_ok))
    except Exception as e:
        print(f"\n❌ UPDATE test failed: {e}")
        results.append(("UPDATE", False))

    # Test DELETE
    try:
        delete_ok = test_delete_todo(todo_id)
        results.append(("DELETE", delete_ok))
    except Exception as e:
        print(f"\n❌ DELETE test failed: {e}")
        results.append(("DELETE", False))

    # Print summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All CRUD tests passed!")
        print("\nAPI Documentation: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit(main())
