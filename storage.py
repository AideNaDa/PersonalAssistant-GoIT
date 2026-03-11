from models.note_book import NoteBook, Note
from models.address_book import AddressBook, Record
import json

FILENAME = "data.json"


def save_data(address_book: AddressBook, notebook: NoteBook):
    combined_data = {
        "contacts": {
            name: record.to_dict()
            for name, record in address_book.data.items()
        },
        "notes": {
            title: note.to_dict() for title, note in notebook.data.items()
        },
    }

    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)


def load_data() -> tuple[AddressBook, NoteBook]:
    notebook = NoteBook()
    address_book = AddressBook()

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            full_data = json.load(f)

            # Uploading contacts
            contacts = full_data.get("contacts", {})
            for record_data in contacts.values():
                address_book.add_record(
                    address_book.add_record(Record.from_dict(record_data))
                )

            # Uploading notes
            notes = full_data.get("notes", {})
            for note_data in notes.values():
                notebook.add_note(Note.from_dict(note_data))

    except (FileNotFoundError, json.JSONDecodeError):
        # If the file is missing or empty/corrupted
        print("The data file was not found or is empty.")

    return address_book, notebook
