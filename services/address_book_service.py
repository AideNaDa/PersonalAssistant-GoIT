from datetime import date, datetime
from typing import Optional

from models.address_book import Record, DATE_FORMAT


def add_contact(
    address_book,
    name: str,
    phone: str,
    email: Optional[str] = None,
    birthday: Optional[str] = None,
    address: Optional[str] = None,
) -> str:
    
    """
    Create a new contact or add data to an existing one.
    Required:
        name, phone
    Optional:
        email, birthday, address
    """
    record = address_book.find(name)

    if record is None:
        try:
            record = Record(name)
            address_book.add_record(record)
        except ValueError as error:
            return str(error)

    messages = []

    try:
        record.add_phone(phone)
        messages.append(f"Phone '{phone}' added.")
    except ValueError as error:
        messages.append(str(error))

    if email is not None:
        try:
            record.add_email(email)
            messages.append(f"Email '{email}' added.")
        except ValueError as error:
            messages.append(str(error))

    if birthday is not None:
        try:
            record.add_birthday(birthday)
            messages.append(f"Birthday '{birthday}' added.")
        except ValueError as error:
            messages.append(str(error))

    if address is not None:
        try:
            record.add_address(address)
            messages.append("Address added.")
        except ValueError as error:
            messages.append(str(error))

    return " ".join(messages)


def delete_address(address_book, name: str) -> str:
    
    """
    Delete address for a contact.
    """
    record = address_book.find(name)

    if record is None:
        return f"Contact '{name}' not found."

    if record.address is None:
        return f"Contact '{name}' has no address."

    record.address = None
    return f"Address deleted for contact '{name}'."


def delete_birthday(address_book, name: str) -> str:
    
    """
    Delete birthday for a contact.
    """
    record = address_book.find(name)

    if record is None:
        return f"Contact '{name}' not found."

    if record.birthday is None:
        return f"Contact '{name}' has no birthday."

    record.birthday = None
    return f"Birthday deleted for contact '{name}'."


def birthdays(address_book, days: int = 7) -> str:
    """
    Show contacts whose birthday is within the next `days` days.
    Output:
        Name: <name>, Phone: <phones>, Birthday: <birthday>
    """
    if days < 0:
        return "Number of days must be 0 or greater."

    today = date.today()
    upcoming_contacts = []

    for record in address_book.data.values():
        if record.birthday is None:
            continue

        try:
            birthday_date = datetime.strptime(record.birthday.value, DATE_FORMAT).date()
        except ValueError:
            # Skip broken data if it somehow exists
            continue

        next_birthday = _get_next_birthday_date(birthday_date, today)
        delta_days = (next_birthday - today).days

        if 0 <= delta_days <= days:
            phones = ", ".join(phone.value for phone in record.phones) if record.phones else "No phone"
            upcoming_contacts.append(
                f"Name: {record.name.value}, Phone: {phones}, Birthday: {record.birthday.value}"
            )

    if not upcoming_contacts:
        return f"No birthdays in the next {days} days."

    return "\n".join(upcoming_contacts)


def _get_next_birthday_date(birthday_date: date, today: date) -> date:
    
    """
    Calculate the next birthday date for the current or next year.
    Handles Feb 29 safely for non-leap years.
    """
    try:
        next_birthday = birthday_date.replace(year=today.year)
    except ValueError:
        # For Feb 29 in a non-leap year
        next_birthday = birthday_date.replace(year=today.year, day=28)

    if next_birthday < today:
        try:
            next_birthday = birthday_date.replace(year=today.year + 1)
        except ValueError:
            next_birthday = birthday_date.replace(year=today.year + 1, day=28)

    return next_birthday
