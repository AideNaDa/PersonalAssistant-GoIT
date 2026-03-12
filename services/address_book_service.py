from datetime import datetime, timedelta
from models.address_book import AddressBook, Record


def _add_email(record, email: str) -> str:
    try:
        record.add_email(email)
    except ValueError as error:
        return str(error)
    return f"Email '{email}' added."


def _add_birthday(record, birthday: str) -> str:
    try:
        record.add_birthday(birthday)
    except ValueError as error:
        return str(error)
    return f"Birthday '{birthday}' added."


def _add_address(record, address: str) -> str:
    try:
        record.add_address(address)
    except ValueError as error:
        return str(error)
    return "Address added."


def _is_birthday(value: str) -> bool:
    try:
        datetime.strptime(value, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def add(args, address_book) -> str:
    if len(args) < 2:
        return "Enter name and value to add."

    name = args[0]
    value = " ".join(args[1:]).strip()

    record = address_book.find(name)
    if record is None:
        return f"Contact '{name}' not found."

    if "@" in value:
        return _add_email(record, value)

    if _is_birthday(value):
        return _add_birthday(record, value)

    return _add_address(record, value)
