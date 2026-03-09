from datetime import datetime, timedelta
from models.address_book import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"❌ Error: {e}"
        except KeyError:
            return "❌ Error: Contact not found."
        except IndexError:
            return "❌ Error: Please provide all necessary arguments."

    return inner


@input_error
def add_contact(args, book: AddressBook):
    pass


@input_error
def change_contact(args, book: AddressBook):
    pass


@input_error
def add_birthday(args, book: AddressBook):
    pass


@input_error
def get_upcoming_birthdays(book: AddressBook):
    pass


@input_error
def add_address(args, book: AddressBook):
    pass


@input_error
def add_email(args, book: AddressBook):
    pass


@input_error
def show_contact(args, book: AddressBook):
    pass


def show_all_contacts(book: AddressBook):
    pass


@input_error
def del_contact(args, book: AddressBook):
    pass
