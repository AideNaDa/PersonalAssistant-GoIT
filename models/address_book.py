import re
import json
from collections import UserDict
from datetime import datetime, timedelta
from typing import Any, Optional, Callable

MAX_NAME_LENGTH = 21
DATE_FORMAT = "%d-%m-%Y"



def input_error(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return f"Контакт '{str(e).strip()}' не знайдено."
        except IndexError:
            return "Недостатньо аргументів для команди."
    return inner


class Field:
    """Base class for contact fields."""

    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    """Contact name with basic validation."""
    
    def __init__(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Будь ласка, введіть ім'я.")
        if len(value) > MAX_NAME_LENGTH:
            raise ValueError(
                f"Name must be at most {MAX_NAME_LENGTH} characters long."
            )
        super().__init__(value)

class Phone(Field):
    """Phone number with regional code validation."""
    
    def __init__(self, value: str) -> None:
        value = value.strip()
        normalized_value = self._normalize(value)
        if not (10 <= len(re.sub(r'\D', '', normalized_value)) <= 15):
            raise ValueError("Номер телефону має містити від 10 до 15 цифр і може починатися з +")
        super().__init__(normalized_value)

    @staticmethod
    def _normalize(value: str) -> str:
        normalized = re.sub(r'(?<!^)\+|[^\d+]', '', value.strip())
        return normalized

class Email(Field):
        """Email with regex validation."""
    
    def __init__(self, value: str) -> None:
        value = value.strip().lower()
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

class Address(Field):
     """Contact physical address."""
    
    def __init__(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Please enter address")
        super().__init__(value)

class Birthday(Field):
    """Birthday field with date validation."""
    
    def __init__(self, value: str) -> None:
        try:
            date_obj = datetime.strptime(value, DATE_FORMAT).date()
            super().__init__(date_obj)
        except ValueError:
            raise ValueError(
                f"Invalid date format. Use {DATE_FORMAT.replace('%', '')}."
                            )
        super().__init__(date_obj)


class Record:
      """Represents a contact record with various fields."""
    
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.address: Optional[Address] = None
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: str) -> None:
        normalized = Phone._normalize(phone)
        if any(p.value == normalized for p in self.phones):
            raise ValueError(f"Phone {phone} not found in this contact.")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        phone_obj = self.find_phone(phone)
        if not phone_obj:
            raise ValueError(f"Номер {phone} не знайдено.")
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        phone_obj = self.find_phone(old_phone)
        if phone_obj is None:
            raise ValueError(f"Phone {old_phone} not found in this contact.")
        Phone(new_phone)  # Validate new phone first
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone: str) -> Optional[Phone]:
        normalized = Phone._normalize(phone)
        return next((p for p in self.phones if p.value == normalized), None)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        email_clean = email.strip().lower()
        if any(e.value == email_clean for e in self.emails):
            raise ValueError("Email already exists")
        self.emails.append(Email(email_clean))

    def remove_email(self, email: str) -> None:
        email_obj = self.find_email(email)
        if not email_obj:
            raise ValueError(f"Email {email} not found in this contact.")
        self.emails.remove(email_obj)

    def edit_email(self, old_email: str, new_email: str) -> None:
        email_obj = self.find_email(old_email)
        if email_obj is None:
            raise ValueError(f"Email {old_email} not found in this contact.")
        Email(new_email)  # Валідація нового email
        self.remove_email(old_email)
        self.add_email(new_email)

    def find_email(self, email: str) -> Optional[Email]:
        email_clean = email.strip().lower()
        for e in self.emails:
            if e.value == email_clean:
                return e
        return None

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def days_to_birthday(self) -> Optional[int]:
        if not self.birthday:
            return None
        today = datetime.today().date()
        try:
            next_bday = self.birthday.value.replace(year=today.year)
        except ValueError:
            next_bday = self.birthday.value.replace(year=today.year, month=3, day=1)
        if next_bday < today:
            try:
                next_bday = next_bday.replace(year=today.year + 1)
            except ValueError:
                next_bday = next_bday.replace(year=today.year + 1, month=3, day=1)
        return (next_bday - today).days


    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "birthday": self.birthday.value.strftime(DATE_FORMAT) if self.birthday else None,
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
        phones = "; ".join(p.value for p in self.phones)
        emails = "; ".join(e.value for e in self.emails)
        birthday = self.birthday.value.strftime(DATE_FORMAT) if self.birthday else "N/A"
        address = self.address.value if self.address else "N/A"
        
        return (f"Contact name: {self.name.value}, "
                f"phones: {phones if phones else 'N/A'}, "
                f"emails: {emails if emails else 'N/A'}, "
                f"birthday: {birthday}, "
                f"address: {address}")


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

            # Search by phone
            if any(query in str(phone) for phone in record.phones):
                results.append(record)
                continue

            # Search by email
            if any(query in str(email).lower() for email in record.emails):
                results.append(record)
                continue

            # Search by address
            if record.address and query in str(record.address).lower():
                results.append(record)
                continue

        return results

    def get_upcoming_birthdays(self) -> list[dict]:
        upcoming = []
        today = datetime.today().date()
        for r in self.data.values():
            days_left = r.days_to_birthday()
            if days_left is not None and 0 <= days_left <= 7:
                upcoming.append({
                    "name": r.name.value, 
                    "birthday": r.birthday.value.strftime(DATE_FORMAT), 
                    "days_left": days_left
                })
        return sorted(upcoming, key=lambda x: x["days_left"])

    def save(self) -> None:
        json_data = {n: r.to_dict() for n, r in self.data.items()}
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def load(self) -> None:
        try:
            with open(FILENAME, "r", encoding="utf-8") as f:
                content = json.load(f)
                self.data = {n: Record.from_dict(r) for n, r in content.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

