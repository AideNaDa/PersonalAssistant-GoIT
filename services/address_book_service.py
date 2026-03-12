from datetime import date, datetime
from typing import Optional, Callable

from models.address_book import AddressBook, Record, DATE_FORMAT


def is_phone(val: str) -> bool:
    return bool(re.fullmatch(r'\d{10}', val))
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
