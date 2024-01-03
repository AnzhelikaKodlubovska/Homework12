from classes import *

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f"Contact {e.args[0]} not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Insufficient information provided."
    return wrapper


@input_error
def saving(data, dict_user):
    if len(data) == 2 and data[0].isalpha():
        name, phone = data
        if name not in dict_user:  
            dict_user[name] = phone
            return f"Contact added."
        else:
            return f"Contact {name} already exists."
    else:
        return "Invalid data provided."


@input_error
def change_phone_number(data, dict_user):
    if len(data) == 2:
        name, new_phone = data
        if name in dict_user:
            dict_user[name] = new_phone
            return f'Phone updated.'
        else:
            return f"Contact {name} not found."
    else:
        return "Insufficient information provided."


@input_error
def show_phone_number(data, dict_user):
    name = ' '.join(data)
    if name in dict_user:
        return f"Phone number for {name}: {dict_user[name]}"
    else:
        return f"It's not enougth information."

@input_error
def show_all(dict_user):
    if dict_user:
        return '\n'.join([f"{name}: {phone}" for name, phone in dict_user.items()])
    else:
        return "No contacts available."

@input_error
def hello():
    return "How can I help you?"

@input_error
def good_bye():
    return "Good bye!"


def commands():
    return {
        'hello': hello,
        'add': saving,
        'change': change_phone_number,
        'phone': show_phone_number,
        'show': show_all,
        'good': good_bye,
        'close': good_bye,
        'exit': good_bye
    }

@input_error
def handle_command(command, dict_user):
    parts = command.split()
    action = parts[0]

    if len(parts) > 0 and action in ['add', 'change', 'phone']:
        try:
            if action in ['add', 'change', 'phone']:
                return commands()[action](parts[1:], dict_user)
        except ValueError as e:
            return str(e)
    else:
        if action == 'show':
            if len(parts) == 1:  
                return "It's not enough information."
            elif len(parts) > 1 and parts[1] == 'all':
                return commands()['show'](dict_user)
            else:
                return commands()['show'](parts[1:], dict_user)
        elif action == 'good':
            return "Sorry, I didn't understand you."
        elif action in commands():
            return commands()[action]()
        else:
            return "Sorry, I didn't understand you."


    parts = command.split()
    action = parts[0]

    if len(parts) > 1 and action in ['add', 'change', 'phone']:
        try:
            if action in ['add', 'change', 'phone']:
                return commands()[action](parts[1:], dict_user)
        except ValueError as e:
            return str(e)
    else:
        if action in commands():
            if action == 'show' and len(parts) > 1 and parts[1] == 'all':
                return commands()[action](dict_user)  
            else:
                return commands()[action]()
        else:
            return "Sorry.I didn't understand."


def read_data_from_file(file_name):
    address_book_data = {}
    with open(file_name, 'r') as file:
        for line in file:
            if ':' in line:
                name, phone = line.strip().split(':')
                address_book_data[name] = phone
            else:
                print(f"Issue with line: {line}. It doesn't have the expected format.")
    return address_book_data

def write_data_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for name, phone in data.items():
            file.write(f"{name}:{phone}\n")

def save_contact(data, dict_user):
    name, phone = data
    record = Record(name)
    record.add_phone(phone)
    dict_user[name] = record
    return f"Contact added."

def update_phone_number(data, dict_user):
    name, new_phone = data
    record = dict_user.get(name)
    if record:
        record.phones = [new_phone]
        return f'Phone updated.'
    else:
        return f"Contact {name} not found."

def show_phone(data, dict_user):
    name = ' '.join(data)
    record = dict_user.get(name)
    if record:
        return f"Phone number for {name}: {record.phones[0]}"
    else:
        return f"Contact {name} not found."

def on_program_exit(file_name, dict_user):
    data_to_write = {record.name: record.phones[0] for record in dict_user.values()}
    write_data_to_file(file_name, data_to_write)

def main():
    file_name = "address_book_data.pkl" 
    address_book_data = read_data_from_file(file_name)
    address_book = AddressBook(address_book_data)

    while True:
        question = input('>> ').lower().strip()
        result = handle_command(question, address_book)
        print(result)
        if result == "Good bye!":
            break 

    write_data_to_file(file_name, address_book.data)

if __name__ == '__main__':
    main()