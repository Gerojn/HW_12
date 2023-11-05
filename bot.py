from collections import UserDict
from datetime import datetime
from main import Record, AddressBook


contacts = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Invalid input. Please try again."

    return wrapper

# Функція для виведення привітання


def hello():
    return "How can I help you?"


def goodbye():
    return "Good bye!"

# Функція для додавання нового контакту


@input_error
def add_contact(input_str):
    parts = input_str.split()
    name = parts[1]
    phone = parts[2]
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return f"Contact '{name}' with phone '{phone}' added successfully."

# Функція для зміни номеру телефону контакту


@input_error
def change_phone(input_str):
    parts = input_str.split()
    name = parts[1]
    phone = parts[2]
    record = contacts.find(name)
    if record:
        record.edit_phone(record.phones[0].value, phone)  # Припускаємо, що контакт має лише один номер
        return f"Phone number for '{name}' updated to '{phone}'."
    else:
        return f"Contact '{name}' not found."

# Функція для отримання номеру телефону за іменем контакту


@input_error
def get_phone(input_str):
    name = input_str.split()[1]
    record = contacts.find(name)
    if record:
        return f"The phone number for '{name}' is '{record.phones[0].value}'."
    else:
        return f"Contact '{name}' not found."

# Функція для виведення всіх контактів


def show_all():
    if not contacts:
        return "No contacts found."
    else:
        result = "Contacts:\n"
        for name, record in contacts.data.items():
            result += str(record) + "\n"
        return result


def find_contacts(query):
    found_contacts = {}
    for name, record in contacts.data.items():
        if query.lower() in name.lower():
            found_contacts[name] = record
        for phone in record.phones:
            if query in phone.value:
                found_contacts[name] = record
    return found_contacts


# Головна функція взаємодії з користувачем
def main():
    global contacts  # Оголошуємо 'contacts' як глобальну змінну
    contacts = AddressBook()  # Ініціалізуємо 'contacts' в цій функції
    while True:
        command = input("Enter a command: ").strip().lower()

        if command == "hello":
            print(hello())
        elif command.startswith("add"):
            print(add_contact(command))
        elif command.startswith("change"):
            print(change_phone(command))
        elif command.startswith("phone"):
            print(get_phone(command))
        elif command == "show all":
            print(show_all())
        elif command == "save":
            file_path = input("Enter the file path to save the address book: ")
            contacts.save_to_file(file_path)
            print(f"Address book saved to {file_path}")
        elif command.startswith("load"):
            file_path = input("Enter the file path to load the address book from: ")
            contacts = AddressBook.load_from_file(file_path)
            print(f"Address book loaded from {file_path}")
        elif command.startswith("find"):
            query = command[5:].strip()
            found_contacts = find_contacts(query)
            if found_contacts:
                for name, record in found_contacts.items():
                    print(record)
            else:
                print("No matching contacts found.")
        elif command in ["good bye", "close", "exit"]:
            print(goodbye())
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
