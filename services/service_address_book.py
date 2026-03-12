from datetime import datetime
import re
from models.address_book import Email, Birthday, Address


def find_record(address_book, name):
    return address_book.data.get(name)


def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_birthday(birthday: str) -> bool:
    try:
        datetime.strptime(birthday, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def add_address(address_book, name: str, address: str) -> str:
    record = find_record(address_book, name)

    if record is None:
        return f"Contact '{name}' not found."

    record.address = Address(address)
    return f"Address added for contact '{name}'."


def add_email(address_book, name: str, email: str) -> str:
    record = find_record(address_book, name)

    if record is None:
        return f"Contact '{name}' not found."

    if not validate_email(email):
        return "Invalid email format."

    for existing_email in record.emails:
        if existing_email.value == email:
            return f"Email '{email}' already exists for contact '{name}'."

    record.emails.append(Email(email))
    return f"Email '{email}' added for contact '{name}'."


def add_birthday(address_book, name: str, birthday: str) -> str:
    record = find_record(address_book, name)

    if record is None:
        return f"Contact '{name}' not found."

    if not validate_birthday(birthday):
        return "Invalid birthday format. Use DD.MM.YYYY"

    record.birthday = Birthday(birthday)
    return f"Birthday added for contact '{name}'."