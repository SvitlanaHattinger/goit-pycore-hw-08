from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y")
            self.value = birthday_date
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return "Phone removed."
        return "Phone not found."

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return "Phone updated."
        return "Old phone not found."

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)

        birthday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday
            else "No birthday"
        )

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"birthday: {birthday}"
        )


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()

        upcoming = []

        for record in self.data.values():

            if record.birthday:

                birthday = record.birthday.value.date()

                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(
                        year=today.year + 1
                    )

                days_left = (birthday_this_year - today).days

                if 0 <= days_left <= 7:

                    congratulation_date = birthday_this_year

                    if congratulation_date.weekday() >= 5:
                        congratulation_date += timedelta(
                            days=7 - congratulation_date.weekday()
                        )

                    upcoming.append(
                        {
                            "name": record.name.value,
                            "congratulation_date":
                                congratulation_date.strftime("%d.%m.%Y"),
                        }
                    )

        return upcoming


def input_error(func):

    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except ValueError as e:
            return str(e)

        except KeyError:
            return "Contact not found."

        except IndexError:
            return "Give me name and phone please."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()

    cmd = cmd.strip().lower()

    return cmd, args


@input_error
def add_contact(args, book):

    name, phone = args

    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    else:
        message = "Contact updated."

    record.add_phone(phone)

    return message


@input_error
def change_contact(args, book):

    name, old_phone, new_phone = args

    record = book.find(name)

    if record is None:
        return "Contact not found."

    return record.edit_phone(old_phone, new_phone)


@input_error
def show_phone(args, book):

    name = args[0]

    record = book.find(name)

    if record is None:
        return "Contact not found."

    return "; ".join(phone.value for phone in record.phones)


def show_all(book):

    if not book.data:
        return "No contacts saved."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):

    name, birthday = args

    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_birthday(birthday)

    return "Birthday added."


@input_error
def show_birthday(args, book):

    name = args[0]

    record = book.find(name)

    if record is None:
        return "Contact not found."

    if record.birthday is None:
        return "Birthday not set."

    return record.birthday.value.strftime("%d.%m.%Y")


def birthdays(args, book):

    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays."

    result = []

    for item in upcoming:
        result.append(
            f"{item['name']} -> {item['congratulation_date']}"
        )

    return "\n".join(result)


def main():

    book = AddressBook()

    print("Welcome to the assistant bot!")

    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
    }

    while True:

        user_input = input("Enter a command: ")

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "all":
            print(show_all(book))

        elif command in commands:
            print(commands[command](args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()