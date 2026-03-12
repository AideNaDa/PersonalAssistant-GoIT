from models.address_book import Record


def add_contact(
    address_book,
    name: str,
    phone: str,
    email: str | None = None,
    birthday: str | None = None,
    address: str | None = None,
) -> str:

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

    if email:
        try:
            record.add_email(email)
            messages.append(f"Email '{email}' added.")
        except ValueError as error:
            messages.append(str(error))

    if birthday:
        try:
            record.add_birthday(birthday)
            messages.append(f"Birthday '{birthday}' added.")
        except ValueError as error:
            messages.append(str(error))

    if address:
        try:
            record.add_address(address)
            messages.append(f"Address '{address}' added.")
        except ValueError as error:
            messages.append(str(error))

    return " ".join(messages)
