from storage import load_data, save_data
from cli import run_cli


def main():
    address_book, notebook = load_data()
    run_cli(address_book, notebook)
    save_data(address_book, notebook)
    print("Data saved.")


if __name__ == "__main__":
    main()
