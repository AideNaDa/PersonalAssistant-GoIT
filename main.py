from storage import load_data, save_data
from cli import run_cli


def main():
    book = load_data()
    run_cli(book)
    save_data(book)
    print("Data saved.")


if __name__ == "__main__":
    main()
