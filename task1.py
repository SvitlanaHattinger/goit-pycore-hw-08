import pickle


class AddressBook:
    pass


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)

    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()

    while True:
        command = input(">>> ")

        if command == "close" or command == "exit":
            save_data(book)
            print("Good bye!")
            break


main()