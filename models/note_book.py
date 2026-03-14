from collections import UserDict
from models.address_book import Field
import textwrap

MAX_TITLE_LENGTH = 26
TITLE_COL = 26
TEXT_COL = 60
TAGS_COL = 25
HEADER_NOTE = (
    f"{'Title':<{TITLE_COL}} "
    f"| {'Text':<{TEXT_COL}} "
    f"| {'Tags':<{TAGS_COL}}"
)
SEPARATOR_NOTE = "-" * len(HEADER_NOTE)


class Title(Field):
    """Note title with length validation."""

    def __init__(self, value: str) -> None:
        if len(value) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title must be at most {MAX_TITLE_LENGTH} characters long."
            )
        super().__init__(value)


class Body(Field):

    pass


class Tag(Field):
    """Note tag with basic equality and hashing for set operations."""

    def __eq__(self, other):
        return isinstance(other, Tag) and self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Note:
    """Note with title, text, and tags."""

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

        tags = (
            ", ".join(tag.value for tag in self.tags)
            if self.tags
            else "No tags"
        )

        text_lines = textwrap.wrap(self.text.value, width=TEXT_COL) or [""]
        tag_lines = textwrap.wrap(tags, width=TAGS_COL) or [""]

        rows = max(len(text_lines), len(tag_lines), 1)

        lines = []

        for i in range(rows):

            title_part = self.title.value if i == 0 else ""
            text_part = text_lines[i] if i < len(text_lines) else ""
            tag_part = tag_lines[i] if i < len(tag_lines) else ""

            line = (
                f"{title_part:<{TITLE_COL}} "
                f"| {text_part:<{TEXT_COL}} "
                f"| {tag_part:<{TAGS_COL}}"
            )

            lines.append(line)
        lines.append(SEPARATOR_NOTE)

        return "\n".join(lines)


class NoteBook(UserDict):
    """Container for notes."""

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
