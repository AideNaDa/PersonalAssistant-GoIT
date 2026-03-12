from models.address_book import Record

def _add_phone(record, phone: str) -> str:
    try:
        record.add_phone(phone)
        return f"Phone '{phone}' added."
    except ValueError as error:
        return str(error)


def _add_email(record, email: str) -> str:
    try:
        record.add_email(email)
        return f"Email '{email}' added."
    except ValueError as error:
        return str(error)


def _add_birthday(record, birthday: str) -> str:
    try:
        record.add_birthday(birthday)
        return f"Birthday '{birthday}' added."
    except ValueError as error:
        return str(error)


def _add_address(record, address: str) -> str:
    try:
        record.add_address(address)
        return f"Address '{address}' added."
    except ValueError as error:
        return str(error)


def add(args, address_book) -> str:
    if not args:
        return "Enter the contact name."

    name = args[0]
    values = args[1:]

    record = address_book.find(name)

    if record is None:
        record = Record(name)
        address_book.add_record(record)
        if not values:
            return f"Contact '{name}' created."

    messages = []

    for value in values:
        if "@" in value:
            messages.append(_add_email(record, value))
        else:
            try:
                messages.append(_add_phone(record, value))
            except ValueError:
                try:
                    messages.append(_add_birthday(record, value))
                except ValueError:
                    messages.append(_add_address(record, value))

    return " ".join(messages)
