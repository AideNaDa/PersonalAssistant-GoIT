from collections import UserDict
from models.address_book import Field
import textwrap

MAX_TITLE_LENGTH = 26


class Title(Field):
    def __init__(self, value: str) -> None:
        if len(value) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title must be at most {MAX_TITLE_LENGTH} characters long."
            )
        super().__init__(value)


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

        wrapped = textwrap.wrap(self.text.value, width=58)

        lines = []
        for i, line in enumerate(wrapped):
            if i == 0:
                lines.append(f"Title: {self.title.value:<26} | Text: {line}")
            else:
                lines.append(f"{'':<33} | {line}")

        sep_bolt = "=" * 100
        sep = "-" * 100

        body = "\n".join(lines)

        return "\n".join([sep_bolt, body, sep, tags_str, sep_bolt])


class NoteBook(UserDict):
    def add_note(self, note: Note):
        if self.find(note.title.value):
            raise ValueError("Note with this title is already exists")
        self.data[note.title.value.lower()] = note

    def find(self, title: str) -> Note | None:
        return self.data.get(title.lower())

    def delete(self, title: str):
        if title in self.data:
            del self.data[title.lower()]
            return f"Note with title '{title}' has been deleted"
        else:
            raise KeyError(f"Note with title '{title}' not found.")
