import pytest
from tests.ui.calculator import Calculator


class TestQuickCalculations:
    """Швидкі тести обчислень"""

    @pytest.mark.unit
    def test_quick_add(self, fast_calculator):
        """Швидкий тест додавання"""
        assert fast_calculator.add(1, 1) == 2

    @pytest.mark.test
    def test_quick_multiply(self, fast_calculator):
        """Швидкий тест множення"""
        assert fast_calculator.multiply(3, 4) == 12

    @pytest.mark.test
    @pytest.mark.parametrize("x,y", [(1, 2), (3, 4), (5, 6)])
    def test_parametrized_quick(self, fast_calculator, x, y):
        """Параметризований швидкий тест"""
        result = fast_calculator.add(x, y)
        assert result == x + y


# Async тести (потребують pytest-asyncio)
@pytest.mark.asyncio
async def test_async_operation():
    """Асинхронний тест"""
    import asyncio

    async def async_add(a, b):
        await asyncio.sleep(0.01)
        return a + b

    result = await async_add(2, 3)
    assert result == 5