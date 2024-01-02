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
            
    def add(self, name, phones, birthday=None):
        record = Record(name, birthday)
        for phone in phones:
            record.add_phone(phone)
        self.add_record(record)

    def change(self, name, old_phone, new_phone):
        record = self.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
        else:
            raise ValueError("Contact not found")

    def phone(self, name):
        record = self.find(name)
        if record:
            return [str(phone) for phone in record.phones]
        else:
            return None

    def find(self, name):
        return self.data.get(name)

    def show_all(self):
        return list(self.data.values())

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

phones = ["1112223333", "4445556666"]
address_book.add("Jane Smith", phones, "1995-12-12")

address_book.change("Jane Smith", "1112223333", "7778889999")

print(address_book.phone("Jane Smith"))

result = address_book.find("Alice Smith")
if result:
    print(f"Found contact: {result.name} - {result.phones}")

all_contacts = address_book.show_all()
for contact in all_contacts:
    print(contact.name, contact.phones)
