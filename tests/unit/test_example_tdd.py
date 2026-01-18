"""Example test demonstrating TDD workflow.

TDD Cycle (Red-Green-Refactor):
1. RED: Write a failing test
2. GREEN: Write minimum code to pass
3. REFACTOR: Improve code while keeping tests green
"""
import pytest


# ============================================================================
# Example 1: Simple function testing
# ============================================================================

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def test_add_positive_numbers():
    """Test adding positive numbers."""
    assert add(2, 3) == 5
    assert add(10, 20) == 30


def test_add_negative_numbers():
    """Test adding negative numbers."""
    assert add(-1, -1) == -2
    assert add(-5, 3) == -2


# ============================================================================
# Example 2: Parameterized testing
# ============================================================================

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (2, 3, 5),
    (10, -5, 5),
    (0, 0, 0),
    (-1, -1, -2),
])
def test_add_parameterized(a, b, expected):
    """Test add function with multiple parameter combinations."""
    assert add(a, b) == expected


# ============================================================================
# Example 3: Testing with fixtures
# ============================================================================

@pytest.fixture
def calculator_data():
    """Fixture providing test data for calculator tests."""
    return {
        "operand1": 10,
        "operand2": 5,
        "add_result": 15,
        "subtract_result": 5,
    }


def test_with_fixture(calculator_data):
    """Test using fixture data."""
    result = add(calculator_data["operand1"], calculator_data["operand2"])
    assert result == calculator_data["add_result"]


# ============================================================================
# Example 4: Testing exceptions
# ============================================================================

def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def test_divide_by_zero():
    """Test that dividing by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_divide_valid():
    """Test valid division."""
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0


# ============================================================================
# Example 5: Class-based tests
# ============================================================================

class TestCalculator:
    """Group related tests in a class."""

    def test_addition(self):
        """Test addition."""
        assert add(1, 1) == 2

    def test_division(self):
        """Test division."""
        assert divide(10, 2) == 5.0

    @pytest.mark.parametrize("a,b", [(0, 0), (1, 0)])
    def test_division_edge_cases(self, a, b):
        """Test division edge cases."""
        if b == 0:
            with pytest.raises(ValueError):
                divide(a, b)
        else:
            assert divide(a, b) == 0.0
