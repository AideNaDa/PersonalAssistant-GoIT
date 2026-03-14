from datetime import date, datetime, timedelta
from typing import Optional, Callable
import re

from models.address_book import (
    AddressBook,
    Record,
    DATE_FORMAT,h
    Birthday,
    Address,
    HEADER,
    SEPORATOR,
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
        try:
            days = int(args[0])
            if days < 0:
                raise ValueError("Number of days must be 0 or greater.")
        except ValueError:
            raise ValueError("Please provide a valid integer for days.")

    today = date.today()
    result = [SEPORATOR, HEADER, SEPORATOR]

    for record in book.data.values():
        if record.birthday is None:
            continue

        birthday_date = record.birthday.value
        next_birthday = _get_next_birthday(birthday_date, today)
        delta_days = (next_birthday - today).days

        if 0 <= delta_days <= days:
            result.append(str(record))

    if not result:
        return f"No birthdays in the next {days} days."

    return "\n".join(result)


def find(args: list[str], book: AddressBook) -> str:
    """Search contacts by partial match in name, phone, email or address."""
    query = args[0].lower()
    results = []
    for record in book.data.values():
        if query in str(record.name).lower():
            results.append(str(record))
            continue

        # Пошук по телефонах
        if any(query in str(phone) for phone in record.phones):
            results.append(str(record))
            continue

        # Пошук по email
        if any(query in str(email).lower() for email in record.emails):
            results.append(str(record))
            continue

        # Пошук по адресі
        if record.address and query in str(record.address).lower():
            results.append(str(record))
            continue

    return "\n".join(results)


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    """Display all contacts in a formatted table layout."""
    
    if not book.data:
        return "Address book is empty."

    n_w, p_w, e_w, a_w, b_w = 15, 15, 20, 20, 12
    
    header = (
        f"{'Name':<{n_w}} | {'Phone':<{p_w}} | {'Email':<{e_w}} | "
        f"{'Address':<{a_w}} | {'Birthday':<{b_w}}"
    )
    separator = "-" * len(header)
    
    result = [separator, header, separator]

    for name in sorted(book.data.keys(), key=str.lower):
        record = book.data[name]
        
        phones = ", ".join([p.value for p in record.phones]) if record.phones else "N/A"
        emails = ", ".join([e.value for e in record.emails]) if record.emails else "N/A"
        address = str(record.address) if record.address else "N/A"
        birthday = record.birthday.value.strftime(DATE_FORMAT) if record.birthday else "N/A"

        row = (
            f"{name[:n_w-3] + '...' if len(name) > n_w else name:<{n_w}} | "
            f"{phones[:p_w-3] + '...' if len(phones) > p_w else phones:<{p_w}} | "
            f"{emails[:e_w-3] + '...' if len(emails) > e_w else emails:<{e_w}} | "
            f"{address[:a_w-3] + '...' if len(address) > a_w else address:<{a_w}} | "
            f"{birthday:<{b_w}}"
        )
        result.append(row)

    result.append(separator)
    result.append(f"Total contacts: {len(book.data)}")
    
    return "\n".join(result)

@input_error
def delete(args: list[str], book: AddressBook) -> str:
    if not args:
        raise ValueError("Provide a name.")
    name, *rest = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")

    if not rest:
        del book.data[name]
        return f"Contact '{name}' deleted entirely."

    field = rest[0]
    if is_phone(field):
        record.phones = [p for p in record.phones if p.value != field]
        return "Phone deleted."
    elif is_email(field):
        record.emails = [e for e in record.emails if e.value != field]
        return "Email deleted."
    elif (
        is_date(field)
        and record.birthday
        and record.birthday.to_string() == field
    ):
        record.birthday = None
        return "Birthday deleted."
    elif record.address and record.address.value == field:
        record.address = None
        return "Address deleted."
    else:
        return "Field not found."


@input_error
def edit(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Provide name and new value(s).")
    name, *rest = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")

    if len(rest) == 2:
        old_val, new_val = rest
        if is_phone(old_val) and is_phone(new_val):
            record.phones = [p for p in record.phones if p.value != old_val]
            record.add_phone(new_val)
            return "Phone replaced."
        elif is_email(old_val) and is_email(new_val):
            record.emails = [e for e in record.emails if e.value != old_val]
            record.add_email(new_val)
            return "Email replaced."
    elif len(rest) == 1:
        new_val = rest[0]
        if is_date(new_val):
            record.birthday = Birthday(new_val)
            return "Birthday updated."
    else:
        address_parts = []
        for arg in rest:
            address_parts.append(arg)

        record.address = Address(" ".join(address_parts))
        return "Address updated."

    return "Invalid edit format."
