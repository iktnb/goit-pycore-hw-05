"""Завдання 2: генератор чисел у тексті та підрахунок доходу."""

import re
from collections.abc import Callable, Iterator


# Межі збігу — пробільні символи або початок/кінець тексту.
NUMBER_PATTERN = re.compile(
    r"(?<!\S)[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?(?!\S)"
)


def generator_numbers(text: str) -> Iterator[float]:
    """Поступово повертає числа, відокремлені від решти тексту пробілами."""
    for match in NUMBER_PATTERN.finditer(text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    """Підсумовує числа за допомогою переданої функції-генератора."""
    return sum(func(text), 0.0)


def main():
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income:.2f}")


if __name__ == "__main__":
    main()
