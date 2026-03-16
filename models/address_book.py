import re
from collections import UserDict
from datetime import datetime
from typing import Any

MAX_NAME_LENGTH = 21
DATE_FORMAT = "%d-%m-%Y"
NAME_COL = 21
PHONE_COL = 15
EMAIL_COL = 35
BDAY_COL = 10
ADDR_COL = 35
HEADER = (
    f"{"Name":<{NAME_COL}} "
    f"| {"Phone":<{PHONE_COL}} "
    f"| {"Email":<{EMAIL_COL}} "
    f"| {"Birthday":<{BDAY_COL}} "
    f"| {"Address":<{ADDR_COL}}"
)
SEPARATOR = "-" * len(HEADER)


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
            raise ValueError(
                f"Name must be at most {MAX_NAME_LENGTH} characters long."
            )
        super().__init__(value)


class Phone(Field):
    """Phone number with regional code validation (+, digits, length 10-15)."""

    def __init__(self, value: str) -> None:
        normalized_value = self._normalize(value)
        digits_only = re.sub(r"\D", "", normalized_value)

        if not (10 <= len(digits_only) <= 15):
            raise ValueError(
                "Phone number must contain between 10 and 15 digits."
            )

        super().__init__(normalized_value)

    @staticmethod
    def _normalize(value: str) -> str:
        """Deletes all symbols, leaving only + and digits"""
        value = value.strip()
        normalized = re.sub(r"(?<!^)\+|[^\d+]", "", value)
        return normalized


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
            raise ValueError(
                f"Invalid date format. Use {DATE_FORMAT.replace('%', '')}."
            )
        super().__init__(date_obj)

    def to_string(self) -> str:
        return self.value.strftime(DATE_FORMAT)


class Record:
    """Represents a contact record with various fields."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.emails: list[Email] = []
        self.address: Address | None = None

    def add_phone(self, phone: str) -> None:
        if self.find_phone(phone):
            raise ValueError("Phone already exists")
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str) -> Phone | None:
        normalized_search = Phone._normalize(phone)
        for p in self.phones:
            if p.value == normalized_search:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        if email in [e.value for e in self.emails]:
            raise ValueError("Email already exists")
        self.emails.append(Email(email))

    def find_email(self, email: str) -> Email | None:
        for e in self.emails:
            if e.value == email:
                return e
        return None

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "birthday": (
                self.birthday.value.strftime(DATE_FORMAT)
                if self.birthday
                else None
            ),
            "emails": [email.value for email in self.emails],
            "address": self.address.value if self.address else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Record":
        record = cls(data["name"])
        for phone in data.get("phones", []):
            record.add_phone(phone)
        for email in data.get("emails", []):
            record.add_email(email)
        if data.get("birthday"):
            record.add_birthday(data["birthday"])
        if data.get("address"):
            record.add_address(data["address"])
        return record

    def __str__(self) -> str:
        name = self.name.value
        phones = [p.value for p in self.phones] or [""]
        emails = [e.value for e in self.emails] or [""]

        birthday = (
            self.birthday.value.strftime(DATE_FORMAT) if self.birthday else ""
        )
        address = self.address.value if self.address else ""

        rows = max(len(phones), len(emails), 1)

        lines = []

        for i in range(rows):
            name_part = name if i == 0 else ""
            phone_part = phones[i] if i < len(phones) else ""
            email_part = emails[i] if i < len(emails) else ""
            bday_part = birthday if i == 0 else ""
            addr_part = address if i == 0 else ""

            line = (
                f"{name_part:<{NAME_COL}} "
                f"| {phone_part:<{PHONE_COL}} "
                f"| {email_part:<{EMAIL_COL}} "
                f"| {bday_part:<{BDAY_COL}} "
                f"| {addr_part:<{ADDR_COL}}"
            )

            lines.append(line)
        lines.append(SEPARATOR)
        return "\n".join(lines)


class AddressBook(UserDict):
    """Container for contact records."""

    def __init__(self):
        super().__init__()
        self.syntax_strict = False

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
