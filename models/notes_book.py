from collections import UserDict
from address_book import Field


class Title(Field):

    pass


class Body(Field):

    pass


class Tag(Field):

    pass


class Note:
    def __init__(self, title, text=""):
        self.title = Title(title)
        self.text = Body(text)
        self.tags = []

    def add_tag(self, tag_value):
        self.tags.append(Tag(tag_value))

    def __str__(self):
        tags_str = (
            ", ".join(t.value for t in self.tags) if self.tags else "No tags"
        )
        return (
            f"Title: {self.title}\n" f"Text: {self.text}\n" f"Tags: {tags_str}"
        )


class NotesBook(UserDict):
    def add_note(self, note: Note):
        self.data[note.title.value] = note

    def find_by_tag(self, tag_query):
        results = []
        for note in self.data.values():
            if any(tag.value == tag_query for tag in note.tags):
                results.append(note)
        return results
