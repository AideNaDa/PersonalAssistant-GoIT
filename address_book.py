import re
from collections import UserDict
from datetime import datetime
from typing import Any

MAX_NAME_LENGTH = 21
PHONE_LENGTH = 10
DATE_FORMAT = "%d-%m-%Y"


class Field:
    """Base class for contact fields."""
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Contact name with basic validation."""
    def __init__(self, value: str) -> None:
        if len(value) > MAX_NAME_LENGTH:
            raise ValueError(f"Name must be at most {MAX_NAME_LENGTH} characters long.")
        super().__init__(value)


class Phone(Field): # На дошці Trello названо PhoneNumber, можете перейменувати за потреби
    """Phone number with basic validation."""
    def __init__(self, value: str) -> None:
        if not value.isdigit() or len(value) != PHONE_LENGTH:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)


class Email(Field):
    """Email with regex validation."""
    def __init__(self, value: str) -> None:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Address(Field):
    """Contact physical address."""
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Birthday(Field):
    """Birthday field with date validation."""
    def __init__(self, value: str) -> None:
        try:
            date_obj = datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(f"Invalid date format. Use {DATE_FORMAT.replace('%', '')}.")
        super().__init__(date_obj)


class Record:
    """Represents a contact record with various fields."""
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.email: Email | None = None
        self.address: Address | None = None

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
        Phone(new_phone)  # Validate new phone first
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def add_address(self, address: str) -> None:
        self.address = Address(address)


class AddressBook(UserDict):
    """Container for contact records."""
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> str:
        if name in self.data:
            del self.data[name]
            return f"Contact '{name}' has been deleted"
        else:
            raise KeyError(f"Contact '{name}' not found.")

    def search(self, query: str) -> list[Record]:
        """Search contacts by partial match in name, phone, email or address."""
        query = query.lower()
        results = []
        for record in self.data.values():
            if query in str(record.name).lower():
                results.append(record)
                continue
            
            # Пошук по телефонах
            if any(query in str(phone) for phone in record.phones):
                results.append(record)
                continue
            
            # Пошук по email
            if record.email and query in str(record.email).lower():
                results.append(record)
                continue
                
            # Пошук по адресі
            if record.address and query in str(record.address).lower():
                results.append(record)
                continue
                
        return results