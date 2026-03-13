from services.address_book_service import *
from services.note_book_service import *
from storage import *
import shlex


def parse_input(user_input):
    try:
        parts = shlex.split(user_input)
    except ValueError:
        return "unclosed quotes", []
    cmd, args = parts[0].lower(), parts[1:]
    return cmd, args


# вспомагательная функция вывода инструкции
def display_instruction() -> str:
    help_text = f"""
{'='*100}
            ASSISTANT BOT COMMAND GUIDE  
{'='*100}

  CONTACT MANAGEMENT:
  -------------------
  add [name] <ph> <bd> <addr> <em>  - Create new contact (order doesn't matter)
  add [name] [phone/email]          - Add extra phone or email to contact
  birthdays [days]                  - Shows upcoming birthdays in 'X' days
  del [name]                        - Delete contact completely
  del [name] [field]                - Delete specific phone, email, bd or addr
  edit [name] [old] [new]           - Replace phone/email or update bd/addr
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
                save_data(address_book, notebook)
                break
            case "exit":
                print("Good bye!")
                save_data(address_book, notebook)
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
            case "find":
                print(find(args, address_book))
            case "birthdays":
                print(birthdays(args, address_book))

            # notebook
            case "add-note":
                print(add_note(args, notebook))
            case "add-tag":
                print(add_tag(args, notebook))
            case "del-note":
                print(del_note(args, notebook))
            case "edit-note":
                print(edit_note(args, notebook))
            case "find-note":
                print(find_note(args, notebook))
            case "show-all-note":
                print(show_all_notes(notebook))
