"""Завдання 3 (додаткове): аналіз лог-файлу та фільтрація за рівнем."""

import sys
from datetime import datetime


LOG_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING", "CRITICAL")


def parse_log_line(line: str) -> dict:
    """Розбирає рядок формату YYYY-MM-DD HH:MM:SS LEVEL повідомлення."""
    parts = line.strip().split(maxsplit=3)
    if len(parts) != 4:
        raise ValueError(
            "Очікується формат YYYY-MM-DD HH:MM:SS LEVEL повідомлення."
        )

    date, time, level, message = parts
    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise ValueError("Некоректна дата або час у записі логу.") from error

    level = level.upper()
    if level not in LOG_LEVELS:
        raise ValueError(f"Невідомий рівень логування: {level}.")

    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> list:
    """Завантажує записи; у разі помилки формату вказує номер рядка."""
    logs = []
    with open(file_path, "r", encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            if not line.strip():
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                raise ValueError(f"Рядок {line_number}: {error}") from error
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """Відбирає записи списковим виразом, незалежно від регістру рівня."""
    return [log for log in logs if log["level"] == level.upper()]


def count_logs_by_level(logs: list) -> dict:
    """Повертає кількість записів для кожного рівня, наявного у файлі."""
    counts = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def display_log_counts(counts: dict):
    """Виводить статистику у вигляді таблиці."""
    print("Рівень логування | Кількість")
    print("----------------|----------")
    for level, count in counts.items():
        print(f"{level:<15} | {count}")


def main():
    if len(sys.argv) not in (2, 3):
        print(
            "Використання: python hw03.py <шлях до лог-файлу> [рівень]",
            file=sys.stderr,
        )
        return 1

    level = sys.argv[2].upper() if len(sys.argv) == 3 else None
    if level is not None and level not in LOG_LEVELS:
        print(
            f"Помилка: рівень має бути одним із {', '.join(LOG_LEVELS)}.",
            file=sys.stderr,
        )
        return 1

    try:
        logs = load_logs(sys.argv[1])
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Помилка читання лог-файлу: {error}", file=sys.stderr)
        return 1

    display_log_counts(count_logs_by_level(logs))
    if not logs:
        print("Лог-файл не містить записів.")

    if level is not None:
        print(f"\nДеталі логів для рівня '{level}':")
        filtered_logs = filter_logs_by_level(logs, level)
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")
        if not filtered_logs:
            print("Записів цього рівня немає.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
