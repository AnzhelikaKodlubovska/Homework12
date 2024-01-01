import pickle

class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            print("File not found.")
            self.contacts = []

    def search_contacts(self, search_query):
        found_contacts = []
        for contact in self.contacts:
            if search_query.lower() in contact.name.lower() or search_query in contact.phone:
                found_contacts.append(contact)
        return found_contacts

address_book = AddressBook()

address_book.add_contact(Contact("John", "12345"))
address_book.add_contact(Contact("Ann", "67890"))
address_book.save_to_file("address_book.pkl")

address_book.load_from_file("address_book.pkl")

search_results = address_book.search_contacts("Jo")
for contact in search_results:
    print(f"Name: {contact.name}, Phone: {contact.phone}")
