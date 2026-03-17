from services.address_book_service import (
    add,
    birthdays,
    delete,
    edit,
    find,
    show_all,
)
from services.note_book_service import (
    add_note,
    add_tag,
    delete_note,
    edit_note,
    find_note,
    show_all_notes,
)
from difflib import get_close_matches

import shlex

# List of all commands available in your bot
COMMANDS = [
    "hello",
    "close",
    "exit",
    "help",
    "?",
    "add",
    "birthdays",
    "del",
    "edit",
    "find",
    "show-all",
    "add-note",
    "add-tag",
    "del-note",
    "edit-note",
    "find-note",
    "show-all-note",
]


def suggest_command(user_input: str) -> str:
    """Searches for the command that is most similar in spelling."""

    # n=1 means we want to find the single best match
    # cutoff=0.5 is the sensitivity threshold (ranging from 0 to 1). 0.5 is optimal for errors of 1–2 letters
    matches = get_close_matches(user_input, COMMANDS, n=1, cutoff=0.5)

    if matches:
        return f"Unknown command. Did you mean: '{matches[0]}'?"
    else:
        return "Unknown command. Type 'help' to view the list of commands."


def parse_input(user_input):
    """Parses the user input into a command and its arguments."""

    try:
        parts = shlex.split(user_input)
    except ValueError:
        return "unclosed quotes", []
    cmd, args = parts[0].lower(), parts[1:]
    return cmd, args


# helper function for printing instructions
def display_instruction() -> str:
    """Returns a formatted string with instructions for using the bot."""

    help_text = f"""
{'='*100}
            ASSISTANT BOT COMMAND GUIDE  
{'='*100}

  CONTACT MANAGEMENT:
  -------------------
  add [name] <ph> <bd> <addr:address> <em>  - Create new contact (order doesn't matter)
  add [name] [phone/email]          - Add extra phone or email to contact
  birthdays [days]                  - Shows upcoming birthdays in 'X' days
  del [name]                        - Delete contact completely
  del [name] [field]                - Delete specific phone, email, bd or addr
  edit [name] [old] [new]           - Replace phone/email or update bd/addr:address
  find [query]                      - Search contacts by any field
  show-all                          - Display all saved contacts

  NOTE MANAGEMENT:
  ----------------
  add-note [title] "[text]" <tags>  - Create a note (text in quotes "")
  add-tag [title] [tag1] [tag2]...  - Add one or more tags to a note
  del-note [title]                  - Delete note completely
  del-note [title] [tag]            - Delete specific tag from a note
  edit-note [title] [new_text]      - Update note text
  edit-note [title] [old_t] [new_t] - Replace an old tag with a new one
  find-note [query]                 - Search notes by title or tags
  show-all-note                     - Display all saved notes

  GENERAL:
  --------
  hello                             - Greeting from bot
  close / exit                      - Save data and exit program
  ? / help                          - Show this manual
{'='*100}
    """
    return help_text


def run_cli(address_book, notebook):
    """Main loop for the command-line interface."""

    print("Assistant bot started. Type 'hello' to start or 'exit' to quit.")
    while True:
        try:
            user_input = input("Enter a command: ")
            if not user_input.strip():
                continue
        except KeyboardInterrupt:
            print("\nGood bye!")
            break

        command, args = parse_input(user_input)
        match command:
            case "unclosed quotes":
                print("Invalid input: unclosed quotes.")
                continue
            case "close":
                print("Good bye!")
                break
            case "exit":
                print("Good bye!")
                break
            case "hello":
                print("Hello, enter '?' or 'help' for instruction")
            case "help":
                print(display_instruction())
            case "?":
                print(display_instruction())

            # address book
            case "add":
                print(add(args, address_book))
            case "birthdays":
                print(birthdays(args, address_book))
            case "del":
                print(delete(args, address_book))
            case "edit":
                print(edit(args, address_book))
            case "find":
                print(find(args, address_book))
            case "show-all":
                print(show_all(address_book))

            # notebook
            case "add-note":
                print(add_note(args, notebook))
            case "add-tag":
                print(add_tag(args, notebook))
            case "del-note":
                print(delete_note(args, notebook))
            case "edit-note":
                print(edit_note(args, notebook))
            case "find-note":
                print(find_note(args, notebook))
            case "show-all-note":
                print(show_all_notes(notebook))

            case _:
                print(suggest_command(command))
