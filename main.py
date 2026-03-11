import re
from datetime import datetime, timedelta, date
from functools import wraps
from typing import Any, Callable
from collections import UserDict

from storage import load_data, save_data
from cli import run_cli


MAX_NAME_LENGTH = 21
DATE_FORMAT = "%d-%m-%Y"
WEEKEND_DAYS = (5, 6)


def input_error(func: Callable) -> Callable:
    """Decorator for handling user input errors."""

    @wraps(func)
    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Handle validation and argument errors
            return str(e)
        except KeyError as e:
            # Catches "Contact not found" errors
            return e.args[0]
        except IndexError:
            # In case len(args) was missed somewhere
            return "Enter user name."
        except Exception as e:
            # Any other unforeseen error
            return f"An unexpected error occurred: {e}"

    return inner

class Field:
    """Base class for contact fields."""

    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Phone(Field):
    def __init__(self, value: str) -> None:
        clean_phone = re.sub(r"(?!^\+)\D", "", value)
        pattern = r"^\+?\d{10,15}$"

        if not re.match(pattern, clean_phone):
            raise ValueError(
                "Phone must contain 10–15 digits. Example: +380123456789"
            )

        super().__init__(clean_phone)


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def _normalize_phone(self, phone: str) -> str:
        return re.sub(r"(?!^\+)\D", "", phone)

    def add_phone(self, phone: str) -> None:
        if self.find_phone(phone):
            raise ValueError("Phone already exists")

        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        phone_obj = self.find_phone(phone)

        if phone_obj is None:
            raise ValueError(f"Phone {phone} not found in this contact.")

        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        phone_obj = self.find_phone(old_phone)

        if phone_obj is None:
            raise ValueError(f"Phone {old_phone} not found in this contact.")

        Phone(new_phone)  # validate new phone

        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        normalized = self._normalize_phone(phone)

        for p in self.phones:
            if p.value == normalized:
                return p

        return None



def main():
    book = load_data()
    run_cli(book)
    save_data(book)
    print("Data saved.")


if __name__ == "__main__":
    main()
