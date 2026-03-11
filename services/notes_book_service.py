from models.note_book import NoteBook, Note
from address_book_service import input_error


@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Provide title and text. Enclose text in quotes.")
    title, text, *tags = args
    if title in notebook:
        raise
    note = Note(title, text)
    for tag in tags:
        note.add_tag(tag)
    notebook.add_note(note)
    return f"Note '{title}' created."


@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Provide title and new text or tags.")
    title, *rest = args
    note = notebook.find(title)
    if not note:
        raise KeyError("Note not found.")

    if len(rest) == 1:
        note.text.value = rest[0]
        return "Note text updated."
    elif len(rest) == 2:
        old_tag, new_tag = rest
        if old_tag in note.tags:
            note.tags.remove(old_tag)
            note.add_tag(new_tag)
            return "Tag replaced."

    return "Invalid edit format."


@input_error
def find_note(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise ValueError("Provide a query.")
    elif len(args) == 1:
        return str(notebook.find(args[0].casefold()))
    else:
        results = []
        for note in notebook.data.values():
            tags_lower = [t.casefold() for t in note.tags.value]
            tags_match = all(arg.casefold() in tags_lower for arg in args)
            if tags_match:
                results.append(str(note))

        return "\n".join(results) if results else "No matches found."


def show_all_notes(notebook: NoteBook) -> str:
    if not notebook.data:
        return "Notebook is emty."
    results = [str(note) for note in notebook.data.values()]
    return "\n".join(results)


@input_error
def add_tag(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Provide title and at least one tag.")
    title, *tags = args
    note = notebook.find(title)
    if not note:
        raise KeyError("Note not found.")
    for tag in tags:
        note.add_tag(tag)
    return f"Tags added to '{title}'."


@input_error
def del_note(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise ValueError("Provide title.")
    title, *tags = args
    note = notebook.find(title)
    if not note:
        raise KeyError("Note not found.")

    if not tags:
        del notebook.data[title]
        return f"Note '{title}' deleted."

    for tag in tags:
        note.delete_tag(tag)
    return "Tag(s) deleted."
