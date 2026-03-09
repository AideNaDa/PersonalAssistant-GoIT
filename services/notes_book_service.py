from models.notes_book import NotesBook, Note
from address_book_service import input_error


@input_error
def add_note(args, book: NotesBook):
    pass


@input_error
def change_note(args, book: NotesBook):
    pass


@input_error
def find_note(args, book: NotesBook):
    pass


def show_all_notes(book: NotesBook):
    pass


@input_error
def add_tag(args, book: NotesBook):
    pass


@input_error
def del_note(args, book: NotesBook):
    pass
