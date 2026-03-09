from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Email(Field):
    pass


class Birthday(Field):
    pass


class Address(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
