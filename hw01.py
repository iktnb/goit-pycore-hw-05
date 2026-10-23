"""Завдання 1: рекурсивні числа Фібоначчі з кешем у замиканні."""


def caching_fibonacci():
    """Створює окремий кеш та повертає функцію fibonacci(n)."""
    cache = {}

    def fibonacci(n):
        if not isinstance(n, int):
            raise TypeError("Номер числа Фібоначчі має бути цілим числом.")
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        # Обидва рекурсивні виклики використовують спільний кеш замикання.
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


def main():
    fib = caching_fibonacci()
    print(fib(10))
    print(fib(15))


if __name__ == "__main__":
    main()
