from collections import UserDict
from datetime import datetime
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
        

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        value = value.strip()
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits.")
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        value = value.strip()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(pattern, value) is None:
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        value = value.strip()
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")
        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Address cannot be empty.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        for existing_phone in self.phones:
            if existing_phone.value == new_phone.value:
                raise ValueError(f"Phone '{phone}' already exists.")
        self.phones.append(new_phone)

    def add_email(self, email):
        new_email = Email(email)
        for existing_email in self.emails:
            if existing_email.value == new_email.value:
                raise ValueError(f"Email '{email}' already exists.")
        self.emails.append(new_email)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_address(self, address):
        self.address = Address(address)

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones) if self.phones else "No phones"
        emails = "; ".join(email.value for email in self.emails) if self.emails else "No emails"
        birthday = self.birthday.value if self.birthday else "No birthday"
        address = self.address.value if self.address else "No address"

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"emails: {emails}, "
            f"birthday: {birthday}, "
            f"address: {address}"
        )
        

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
