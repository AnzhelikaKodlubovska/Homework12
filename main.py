import pickle
from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.value = value

    def __str__(self):
        return str(self.value)

    def is_valid(self, value):
        return True

class Name(Field):
    pass

class Phone(Field):
    def is_valid(self, value):
        return len(str(value)) == 10 and str(value).isdigit()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.is_valid(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid phone number")

class Birthday(Field):
    def is_valid(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.is_valid(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid date format")

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if birthday:
            self.set_birthday(birthday)

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        for p in self.phones:
            if str(p.value) == str(phone):
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if str(p.value) == str(phone):
                return p
        return None

    def set_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already exists")

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday_year = today.year
            birthday_date = datetime.strptime(str(self.birthday.value), '%Y-%m-%d').date().replace(year=next_birthday_year)
            if today > birthday_date:
                birthday_date = birthday_date.replace(year=next_birthday_year + 1)
            return (birthday_date - today).days
        else:
            return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        else:
            return False

    def iterator(self, n):
        record_list = list(self.data.values())
        for i in range(0, len(record_list), n):
            yield record_list[i:i + n]

    def save_to_disk(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)

    @classmethod
    def load_from_disk(cls, file_path):
        address_book = cls()
        try:
            with open(file_path, 'rb') as file:
                address_book.data = pickle.load(file)
        except FileNotFoundError:
            pass
        return address_book

    def search_contacts(self, query):
        matching_contacts = []
        for record in self.data.values():
            if query in str(record.name) or any(query in str(phone.value) for phone in record.phones):
                matching_contacts.append(record)
        return matching_contacts

address_book = AddressBook()

contact1 = Record("John Doe")
contact1.add_phone("1234567890")
contact1.set_birthday("1990-01-01")
address_book.add_record(contact1)

contact2 = Record("Alice Smith")
contact2.add_phone("9876543210")
contact2.add_phone("5555555555")
contact2.set_birthday("1985-05-05")
address_book.add_record(contact2)

address_book.save_to_disk('address_book_data.pkl')

restored_address_book = AddressBook.load_from_disk('address_book_data.pkl')

query = "John"  
results = restored_address_book.search_contacts(query)
for result in results:
    print(result.name, result.phones)
