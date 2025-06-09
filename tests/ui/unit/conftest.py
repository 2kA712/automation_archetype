import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_database():
    """Мок бази даних для юніт-тестів"""
    mock_db = Mock()
    mock_db.is_connected = True
    mock_db.execute_query.return_value = [{"id": 1, "name": "test"}]
    return mock_db

@pytest.fixture
def fast_calculator():
    """Швидкий калькулятор без історії для юніт-тестів"""
    from tests.ui.calculator import Calculator
    calc = Calculator()
    # Відключаємо історію для швидкості
    calc.history = []
    return calc
