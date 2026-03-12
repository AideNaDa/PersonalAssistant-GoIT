from collections import UserDict
from models.address_book import Field


class Title(Field):

    pass


class Body(Field):

    pass


class Tag(Field):

    pass


class Note:
    def __init__(self, title: str, text: str) -> None:
        self.title = Title(title)
        self.text = Body(text)
        self.tags: set[Tag] = set()

    def add_tag(self, tag: str):
        self.tags.add(Tag(tag))

    def find_tag(self, tag: str) -> bool:
        return Tag(tag) in self.tags

    def delete_tag(self, tag: str):
        if not self.find_tag(tag):
            return f"Tag '{tag}' not found"
        self.tags.discard(Tag(tag))

    def to_dict(self):
        return {
            "title": self.title.value,
            "text": self.text.value,
            "tags": [tag.value for tag in self.tags],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        note = cls(data["title"], data["text"])
        for tag_val in data["tags"]:
            note.add_tag(tag_val)
        return note

    def __str__(self):
        tags_str = (
            ", ".join(t.value for t in self.tags) if self.tags else "No tags"
        )
        return (
            f"Title: {self.title}\n" f"Text: {self.text}\n" f"Tags: {tags_str}"
        )


class NoteBook(UserDict):
    def add_note(self, note: Note):
        if self.find(note.title.value):
            raise ValueError("Note with this title is already exists")
        self.data[note.title.value.lower()] = note

    def find(self, title: str) -> Note | None:
        return self.data.get(title)

    def delete(self, title: str):
        if title in self.data:
            del self.data[title]
            return f"Note with title '{title}' has been deleted"
        else:
            raise KeyError(f"Note with title '{title}' not found.")
