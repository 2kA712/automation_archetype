import time
from typing import Union


class Calculator:
    """Простий калькулятор з різними операціями"""

    def __init__(self):
        self.history = []

    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Додавання двох чисел"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Віднімання двох чисел"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Множення двох чисел"""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Ділення двох чисел"""
        if b == 0:
            raise ValueError("Ділення на нуль неможливе")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def power(self, base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
        """Піднесення до степеня"""
        result = base ** exponent
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result

    def factorial(self, n: int) -> int:
        """Факторіал числа (повільна операція для демонстрації)"""
        if n < 0:
            raise ValueError("Факторіал від'ємного числа не існує")
        if n == 0 or n == 1:
            return 1

        # Штучно сповільнюємо для демонстрації повільних тестів
        time.sleep(0.1)

        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def get_history(self) -> list:
        """Отримання історії операцій"""
        return self.history.copy()

    def clear_history(self):
        """Очищення історії"""
        self.history.clear()