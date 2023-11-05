from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        self.value = None
        self.set_value(value)

        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday format")
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, birthday):
        if not self.validate_birthday(birthday):
            raise ValueError("Invalid birthday format")
        self._value = birthday

    @staticmethod
    def validate_birthday(birthday):
        try:
            datetime.strptime(birthday, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def set_value(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        self.value = None
        self.set_value(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, phone):
        if phone is not None and not self.validate_phone(phone):
            raise ValueError("Invalid phone number format")
        self._value = phone

    @staticmethod
    def validate_phone(phone):
        if phone is not None:
            return len(phone) == 10 and phone.isdigit()
        return False

    def set_value(self, value):
        self.value = value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.month, self.birthday.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day)
            delta = next_birthday - today
            return delta.days
        return None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone = Phone(phone)
        self.phones = [p for p in self.phones if p.value != phone.value]

    def edit_phone(self, old_phone, new_phone):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone.value:
                self.phones[i] = new_phone
                break
            else:
                raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name, None)

    def iterator(self, n=1):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i + n]

    def save_to_file(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)

    @classmethod
    def load_from_file(cls, file_path):
        try:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
            address_book = cls()
            address_book.data = data
            return address_book
        except FileNotFoundError:
            return cls()


# Приклад використання:
if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")


