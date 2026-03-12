from datetime import datetime, timedelta
from models.address_book import Record, DATE_FORMAT, PHONE_LENGTH


def _is_email(value: str) -> bool:
    return "@" in value


def _is_phone(value: str) -> bool:
    return value.isdigit() and len(value) == PHONE_LENGTH


def _is_birthday(value: str) -> bool:
    try:
        datetime.strptime(value, DATE_FORMAT)
        return True
    except ValueError:
        return False


def _add_phone(record, phone: str) -> str:
    try:
        record.add_phone(phone)
    except ValueError as error:
        return str(error)
    return f"Phone '{phone}' added."


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
    return f"Address '{address}' added."


def add(args, address_book) -> str:
    if not args:
        return "Enter the contact name."

    name = args[0]
    values = args[1:]

    record = address_book.find(name)
    created = False

    if record is None:
        try:
            record = Record(name)
            address_book.add_record(record)
            created = True
        except ValueError as error:
            return str(error)

    if not values:
        if created:
            return f"Contact '{name}' created."
        return f"Contact '{name}' already exists."

    messages = []

    for value in values:
        if _is_phone(value):
            messages.append(_add_phone(record, value))
        elif _is_email(value):
            messages.append(_add_email(record, value))
        elif _is_birthday(value):
            messages.append(_add_birthday(record, value))
        else:
            messages.append(_add_address(record, value))

    if created:
        return f"Contact '{name}' created. " + " ".join(messages)

    return " ".join(messages)
