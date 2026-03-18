from datetime import date, datetime, timedelta
from typing import Callable
import re

from models.address_book import (
    AddressBook,
    Phone,
    Record,
    DATE_FORMAT,
    Birthday,
    Address,
    HEADER,
    SEPARATOR,
)


def input_error(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except KeyError:
            return "Error: Contact not found."
        except IndexError:
            return "Error: Please provide all necessary arguments."

    return inner


def is_phone(val: str) -> bool:
    """Checks if the value is a valid phone number (10-15 digits, ignoring non-digit characters)."""
    digits_only = re.sub(r"\D", "", val)
    return 10 <= len(digits_only) <= 15


def is_email(val: str) -> bool:
    """Checks if the value is a valid email address."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", val))


def is_date(val: str) -> bool:
    """Checks if the value is a valid date in the expected format."""
    try:
        datetime.strptime(val, DATE_FORMAT)
        return True
    except ValueError:
        return False


@input_error
def add(args: list[str], book: AddressBook) -> str:
    """Adds a new contact or updates an existing one with provided details. Usage: add <name> [phone/email/birthday/addr:address]. Address must be prefixed with 'addr:' or 'address:'."""

    if len(args) < 1:
        raise ValueError("Provide at least a name.")

    name, *rest = args
    record = book.find(name)
    updated = False

    if not record:
        record = Record(name)
        book.add_record(record)

    address_parts = []
    for arg in rest:
        if is_phone(arg):
            # Check for duplicates
            norm_phone = Phone._normalize(arg)
            if any(p.value == norm_phone for p in record.phones):
                print(f"Phone {arg} is already assigned to {name}.")
                continue
            record.add_phone(arg)
            updated = True
        elif is_email(arg):
            # Check for existing email
            if any(e.value == arg.lower() for e in record.emails):
                print(f"Email {arg} is already assigned to {name}.")
                continue
            record.add_email(arg)
            updated = True
        elif is_date(arg):
            record.birthday = Birthday(arg)
            updated = True
        elif arg.startswith("addr:") or arg.startswith("address:"):
            address_value = arg.split(":", 1)[1].strip()
            if re.search(r'[^a-zA-Zа-яА-Я0-9\s№/.,;:"\'-]', address_value):
                print(
                    f"Address '{address_value}' contains invalid characters. Skipping."
                )
            else:
                address_parts.append(address_value)
        else:
            print(f"Unrecognized argument '{arg}'. Skipping.")

    if address_parts:
        if record.address:
            print(
                f"If you want to update the address, please use the edit command. Current address: {record.address}"
            )
        record.address = Address(" ".join(address_parts))
        updated = True

    if not record.phones and not record.emails and not record.birthday and not record.address:
        return f"Contact '{name}' created."

    if updated:
        return f"Contact '{name}' updated."
    
    return f"No changes made to contact '{name}'."


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
    """Lists contacts with birthdays in the next N days. Usage: birthdays [N]. If N is not provided, defaults to 7 days."""

    days = 7

    if args:
        try:
            days = int(args[0])
            if days < 0:
                raise ValueError("Number of days must be 0 or greater.")
        except ValueError:
            raise ValueError("Please provide a valid integer for days.")

    today = date.today()
    msg = [SEPARATOR, HEADER, SEPARATOR]
    result = []

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
    msg.extend(result)

    return "\n".join(msg)


def find(args: list[str], book: AddressBook) -> str:
    """Search contacts by partial match in name, phone, email or address. Use prefixes like addr: for specific field search."""

    query = args[0].lower()

    query_digits = re.sub(r"\D", "", query)
    results = []
    msg = [SEPARATOR, HEADER, SEPARATOR]

    # Parse prefixes for specific field search
    if query.startswith("name:"):
        search_query = query[5:].strip()
        search_field = "name"
    elif query.startswith("phone:"):
        search_query = query[6:].strip()
        search_field = "phone"
    elif query.startswith("email:"):
        search_query = query[6:].strip()
        search_field = "email"
    elif query.startswith("addr:") or query.startswith("address:"):
        search_query = query.split(":", 1)[1].strip()
        search_field = "address"
    else:
        search_query = query
        search_field = None  # General search

    for record in book.data.values():
        if search_field == "name" or (
            search_field is None and search_query in str(record.name).lower()
        ):
            results.append(str(record))
            continue

        if search_field == "phone" or (
            search_field is None
            and query_digits
            and is_phone(query_digits)
            and any(query_digits in p.value for p in record.phones)
        ):
            results.append(str(record))
            continue

        if search_field == "email" or (
            search_field is None
            and any(
                search_query in str(email).lower() for email in record.emails
            )
        ):
            results.append(str(record))
            continue

        if (
            search_field == "address"
            and record.address
            and search_query in str(record.address).lower()
        ):
            results.append(str(record))
            continue

    if not results:
        return "No matching contacts found."

    msg.extend(results)
    return "\n".join(msg)


@input_error
def show_all(book: AddressBook) -> str:
    """Display all contacts in a formatted table layout."""

    if not book.data:
        return "Address book is empty."

    result = [SEPARATOR, HEADER, SEPARATOR]

    for name in sorted(book.data.keys(), key=str.lower):
        record = book.data[name]

        result.append(str(record))

    result.append(f"Total contacts: {len(book.data)}")
    return "\n".join(result)


@input_error
def delete(args: list[str], book: AddressBook) -> str:
    """Deletes a contact entirely or specific fields from a contact. Usage: del <name> [field]. If no field is provided, the entire contact is deleted."""

    if not args:
        raise ValueError("Provide a name.")
    name, *rest = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")

    if not rest:
        book.delete(name)
        return f"Contact '{name}' deleted entirely."

    field = rest[0]
    if is_phone(field):
        normalized_f = Phone._normalize(field)
        record.phones = [p for p in record.phones if p.value != normalized_f]
        return "Phone deleted."
    elif is_email(field):
        record.emails = [e for e in record.emails if e.value != field]
        return "Email deleted."
    elif field == "birthday":
        record.birthday = None
        return "Birthday deleted."
    elif field in ["address", "adress", "adres", "addres", "addr"]:
        record.address = None
        return "Address deleted."
    else:
        return "Field not found."


@input_error
def edit(args: list[str], book: AddressBook) -> str:
    """Edits a contact's phone, email, birthday or address. Usage: edit <name> <old_value> <new_value> for phones and emails, edit <name> <new_birthday> for birthday, edit <name> <new_address> for address."""

    if len(args) < 2:
        raise ValueError("Provide name and new value(s).")
    name, *rest = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")

    if len(rest) == 2:
        old_val, new_val = rest
        if is_phone(old_val) and is_phone(new_val):
            norm_old = Phone._normalize(old_val)
            norm_new = Phone._normalize(new_val)

            if norm_old not in [p.value for p in record.phones]:
                raise ValueError(
                    "Old phone number not found for this contact."
                )

            if norm_new in [p.value for p in record.phones]:
                raise ValueError(
                    "New phone number already exists for this contact."
                )
            record.phones = [p for p in record.phones if p.value != norm_old]
            record.add_phone(new_val)
            return "Phone replaced."
        elif is_email(old_val) and is_email(new_val):
            if old_val not in [e.value for e in record.emails]:
                raise ValueError(
                    "Old email address not found for this contact."
                )
            if new_val in [e.value for e in record.emails]:
                raise ValueError(
                    "New email address already exists for this contact."
                )
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
            if arg.startswith("addr:") or arg.startswith("address:"):
                address_value = arg.split(":", 1)[1].strip()
                if re.search(r'[^a-zA-Zа-яА-Я0-9\s№/.,;:"\'-]', address_value):
                    print(
                        f"Address '{address_value}' contains invalid characters. Skipping."
                    )
                else:
                    address_parts.append(address_value)
            else:
                print(f"Unrecognized argument '{arg}'. Skipping.")

        record.address = Address(" ".join(address_parts))
        return "Address updated."

    return "Invalid edit format."
