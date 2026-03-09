from services.address_book_service import *
from services.notes_book_service import *
from storage import *


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def run_cli(address_book, note_book):
    print("Assistant bot started. Type 'exit' to quit.")
    while True:
        try:
            user_input = input(">> ")
        except KeyboardInterrupt:
            print("\nGood bye!")
            break
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(...)
            break
        elif command == "hello":
            print("How can I help you?")
