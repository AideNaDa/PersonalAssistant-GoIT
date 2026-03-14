from models.note_book import NoteBook, Note, Tag, SEPARATOR_NOTE, HEADER_NOTE
from services.address_book_service import input_error


@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    """Adds a new note with optional tags. Usage: add-note <title> <text> [tag1 tag2 ...]. Enclose text in quotes if it contains spaces."""

    if len(args) < 2:
        raise ValueError("Provide title and text. Enclose text in quotes.")
    title, text, *tags = args
    note = Note(title, text)

    for tag in tags:
        note.add_tag(tag)
    notebook.add_note(note)
    return f"Note '{title}' created."


@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    """Edits a note's text or replaces a tag. For text: edit-note <title> <new text>. For tags: edit-note <title> <old tag> <new tag>."""

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
        if Tag(old_tag) in note.tags:
            note.tags.remove(Tag(old_tag))
            note.add_tag(new_tag)
            return "Tag replaced."

    return "Invalid edit format."


@input_error
def find_note(args: list[str], notebook: NoteBook) -> str:
    """Finds a note by title or tags. If multiple tags are provided, all must match."""

    if not args:
        raise ValueError("Provide a query.")
    note = notebook.find(args[0])
    if note:
        return str(note)
    else:
        results = []
        for note in notebook.data.values():
            tags_lower = [t.value for t in note.tags]
            tags_match = all(arg in tags_lower for arg in args)
            if tags_match:
                results.append(str(note))

    return "\n".join(results) if results else "No matches found."


def show_all_notes(notebook: NoteBook) -> str:
    """Returns a formatted string of all notes in the notebook."""

    if not notebook.data:
        return "Notebook is empty."

    result = [SEPARATOR_NOTE, HEADER_NOTE, SEPARATOR_NOTE]

    for title in sorted(notebook.data.keys(), key=str.lower):
        note = notebook.data[title]

        result.append(str(note))

    result.append(f"Total notes: {len(notebook.data)}")
    return "\n".join(result)


@input_error
def add_tag(args: list[str], notebook: NoteBook) -> str:
    """Adds one or more tags to an existing note. Usage: add-tag <title> <tag1> [tag2 ...]."""

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
def delete_note(args: list[str], notebook: NoteBook) -> str:
    """Deletes a note entirely or specific tags from a note. Usage: del-note <title> [tag1 tag2 ...]. If no tags are provided, the entire note is deleted."""

    if not args:
        raise ValueError("Provide title.")
    title, *tags = args
    note = notebook.find(title)
    if not note:
        raise KeyError("Note not found.")

    if not tags:
        del notebook.data[title.lower()]
        return f"Note '{title}' deleted."

    for tag in tags:
        note.delete_tag(tag)
    return "Tag(s) deleted."
