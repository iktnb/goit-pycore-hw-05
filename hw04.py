"""Завдання 4: бот контактів з обробкою помилок через декоратор."""

from functools import wraps


def input_error(func):
    """Перетворює помилки обробника на зрозумілі відповіді користувачеві."""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as error:
            return str(error) or "Give me name and phone please."
        except IndexError:
            return "Enter user name."

    return inner


def parse_input(user_input):
    """Повертає команду та аргументи без залежності від регістру."""
    parts = user_input.strip().lower().split()
    if not parts:
        return ("",)
    command, *args = parts
    return command, *args


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name.lower()] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    name = name.lower()
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    # Порожній список спричиняє IndexError, відсутнє ім'я — KeyError.
    name = args[0].lower()
    if len(args) > 1:
        raise ValueError("Enter only one user name.")
    return contacts[name]


@input_error
def show_all(args, contacts):
    if args:
        raise ValueError("The all command takes no arguments.")
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


@input_error
def say_hello(args, contacts):
    if args:
        raise ValueError("The hello command takes no arguments.")
    return "How can I help you?"


@input_error
def close_bot(args, contacts):
    if args:
        raise ValueError("The exit and close commands take no arguments.")
    return "Good bye!"


def main():
    contacts = {}
    handlers = {
        "hello": say_hello,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "exit": close_bot,
        "close": close_bot,
    }
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input = input("Enter a command: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break

        command, *args = parse_input(user_input)
        handler = handlers.get(command)
        if handler is None:
            print("Invalid command.")
            continue

        response = handler(args, contacts)
        print(response)
        if command in ("exit", "close") and not args:
            break


if __name__ == "__main__":
    main()
