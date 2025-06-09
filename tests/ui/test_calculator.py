"""Тести для калькулятора"""
import pytest
import time

class TestBasicOperations:
    """Тести базових операцій калькулятора"""

    @pytest.mark.unit
    def test_addition(self, calculator):
        """Тест додавання"""
        result = calculator.add(2, 3)
        assert result == 5
        assert "2 + 3 = 5" in calculator.get_history()

    @pytest.mark.unit
    def test_subtraction(self, calculator):
        """Тест віднімання"""
        result = calculator.subtract(5, 3)
        assert result == 2

    @pytest.mark.unit
    def test_multiplication(self, calculator):
        """Тест множення"""
        result = calculator.multiply(4, 3)
        assert result == 12

    @pytest.mark.unit
    def test_division(self, calculator):
        """Тест ділення"""
        result = calculator.divide(10, 2)
        assert result == 5

    @pytest.mark.unit
    def test_division_by_zero(self, calculator):
        """Тест ділення на нуль"""
        with pytest.raises(ValueError, match="Ділення на нуль неможливе"):
            calculator.divide(10, 0)


class TestAdvancedOperations:
    """Тести складних операцій"""

    @pytest.mark.unit
    def test_power(self, calculator):
        """Тест піднесення до степеня"""
        result = calculator.power(2, 3)
        assert result == 8

    @pytest.mark.slow
    def test_factorial(self, calculator):
        """Тест факторіала (повільний)"""
        result = calculator.factorial(5)
        assert result == 120

    @pytest.mark.slow
    def test_factorial_zero(self, calculator):
        """Тест факторіала нуля"""
        result = calculator.factorial(0)
        assert result == 1

    @pytest.mark.unit
    def test_factorial_negative(self, calculator):
        """Тест факторіала від'ємного числа"""
        with pytest.raises(ValueError, match="Факторіал від'ємного числа не існує"):
            calculator.factorial(-1)


class TestParametrized:
    """Параметризовані тести"""

    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, 2),
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (10, -5, 5)
    ])
    @pytest.mark.unit
    def test_addition_parametrized(self, calculator, a, b, expected):
        """Параметризований тест додавання"""
        result = calculator.add(a, b)
        assert result == expected

    @pytest.mark.parametrize("operation,a,b,expected", [
        ("add", 2, 3, 5),
        ("subtract", 5, 3, 2),
        ("multiply", 4, 3, 12),
        ("divide", 10, 2, 5),
    ])
    @pytest.mark.unit
    def test_operations_parametrized(self, calculator, operation, a, b, expected):
        """Параметризований тест різних операцій"""
        method = getattr(calculator, operation)
        result = method(a, b)
        assert result == expected


class TestHistory:
    """Тести історії операцій"""

    @pytest.mark.unit
    def test_history_tracking(self, calculator):
        """Тест відстеження історії"""
        calculator.add(1, 2)
        calculator.multiply(3, 4)

        history = calculator.get_history()
        assert len(history) == 2
        assert "1 + 2 = 3" in history
        assert "3 * 4 = 12" in history

    @pytest.mark.unit
    def test_clear_history(self, calculator):
        """Тест очищення історії"""
        calculator.add(1, 2)
        calculator.clear_history()

        assert len(calculator.get_history()) == 0

# Пропуск тестів
@pytest.mark.skip(reason="Функціональність ще не реалізована")
def test_square_root(calculator):
    """Тест квадратного кореня (не реалізовано)"""
    pass

@pytest.mark.skipif(time.time() % 2 == 0, reason="Випадковий пропуск для демонстрації")
def test_random_skip(calculator):
    """Тест з випадковим пропуском"""
    pass

# Очікувані падіння
@pytest.mark.xfail(reason="Відомий баг з точністю float")
def test_float_precision(calculator):
    """Тест точності float (очікуване падіння)"""
    result = calculator.add(0.1, 0.2)
    assert result == 0.3  # Може не пройти через особливості float

@pytest.mark.xfail(strict=True, reason="Має обов'язково падати")
def test_must_fail():
    """Тест, який має падати"""
    assert False, "Цей тест має падати"
