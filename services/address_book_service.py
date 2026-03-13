from datetime import date, datetime, timedelta
from typing import Optional, Callable
import re

from models.address_book import (
    AddressBook,
    Record,
    DATE_FORMAT,
    Birthday,
    Address,
)


def input_error(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"❌ Error: {e}"
        except KeyError:
            return "❌ Error: Contact not found."
        except IndexError:
            return "❌ Error: Please provide all necessary arguments."

    return inner


def is_phone(val: str) -> bool:
    return bool(re.fullmatch(r"\d{10}", val))


def is_email(val: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", val))


def is_date(val: str) -> bool:
    try:
        datetime.strptime(val, DATE_FORMAT)
        return True
    except ValueError:
        return False


@input_error
def add(args: list[str], book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Provide at least a name.")

    name, *rest = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        msg = f"Contact '{name}' created."
    else:
        msg = f"Contact '{name}' updated."

    address_parts = []
    for arg in rest:
        if is_phone(arg):
            record.add_phone(arg)
        elif is_email(arg):
            record.add_email(arg)
        elif is_date(arg):
            record.birthday = Birthday(arg)
        else:
            address_parts.append(arg)

    if address_parts:
        record.address = Address(" ".join(address_parts))

    return msg


def _get_next_birthday(birthday_date: date, today: date) -> date:
    try:
        next_birthday = birthday_date.replace(year=today.year)
    except ValueError:
        next_birthday = birthday_date.replace(year=today.year, day=28)

    if next_birthday < today:
        try:
            next_birthday = birthday_date.replace(year=today.year + 1)
        except ValueError:
            next_birthday = birthday_date.replace(year=today.year + 1, day=28)

    return next_birthday


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    days = 7

    if args:
        days = int(args[0])
        if days < 0:
            raise ValueError("Number of days must be 0 or greater.")

    today = date.today()
    result = []

    for record in book.data.values():
        if record.birthday is None:
            continue

        birthday_date = record.birthday.value
        next_birthday = _get_next_birthday(birthday_date, today)
        delta_days = (next_birthday - today).days

        if 0 <= delta_days <= days:
            phones = ", ".join(phone.value for phone in record.phones) if record.phones else "N/A"
            birthday_str = record.birthday.value.strftime(DATE_FORMAT)

            result.append(
                f"Name: {record.name.value}, Phone: {phones}, Birthday: {birthday_str}"
            )

    if not result:
        return f"No birthdays in the next {days} days."

    return "\n".join(result)
