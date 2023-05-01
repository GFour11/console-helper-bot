from datetime import datetime
import re
from pathlib import Path

from console_bot.classes import Phone, Name, Birthday, Record, AdressBook, Email, Address

address_book = AdressBook.load_data()
iterator = iter(address_book)

def input_error(func):
    '''Decorator that handles errors in the handlers'''
    def inner(*args, **kwargs):
        try:
            output = func(*args, **kwargs)
        except KeyError as ke:
            output = f'There are no contact {str(ke)} in contacts'
        except ValueError as ve:
            output = str(ve).capitalize()
        # except AttributeError as sa:
        #     print(sa)
        #     output = 'There no birthday date in this contact'
        except StopIteration:
            output = 'There are no more contacts'
        return output
    return inner

def hello(*args, **kwargs) -> str:
    '''Return bots greeting'''
    output = 'How can I help you?'
    return output

@input_error
def adding(data: str, *args, **kwargs) -> str:
    '''If contact is existing add phone to it, else create contact'''

    def parse_data(data: str, element: str):
        name_classes = {
            'phone': Phone,
            'email': Email,
            'address': Address,
            'birthday': Birthday
        }
        key_words = '|'.join(name_classes) + '|$'
        match = re.search(rf'\b({element}\:.+)(?=\b({key_words})\b)', data, re.IGNORECASE)
        if match:
            full = match.group(1)
            data = data.replace(full, '').strip()
            class_ = name_classes.get(element)
            value = class_(full.split(':')[1].strip())
            return data, value
        return data, None
            
    data, birthday = parse_data(data, 'birthday')
    data, address = parse_data(data, 'address')
    data, phone = parse_data(data, 'phone')
    data, email = parse_data(data, 'email')
    name = Name(data)
    record: Record = address_book.data.get(name.value)

    if record:
        if birthday:
            record.birthday = birthday
        if address:
            record.address = address
        if email:
            record.email = email
        if phone:
            record.add_phone(phone)
        output = f'To contact {name} add new data'
    else:
        record = Record(name, phone, birthday=birthday, address=address, email=email)
        address_book.add_record(record)
        output = f'Contact {record} is saved'
    return output

@input_error
def changing(data: str, *args, **kwargs) -> str:
    '''Change contact in the dictionary'''
    words = data.split()
    name = ' '.join(words[:-2])
    record = address_book.data[name]
    new_phone = Phone(words[-1])
    old_phone = Phone(words[-2])
    record.change(old_phone, new_phone)
    output = f'Contact {name} is changed from {old_phone} to {new_phone}'
    return output

@input_error
def get_phones(name: str, *args, **kwargs) -> str:
    '''Return numbers received contact'''
    record = address_book.data[name]
    numbers = ', '.join(record.get_numbers())
    return numbers

@input_error
def remove_phone(data: str, *args, **kwargs) -> str:
    '''Remove phone from contact phone numbers'''
    words = data.split()
    name = ' '.join(words[:-1])
    record = address_book.data[name]
    phone = Phone(words[-1])
    record.remove_phone(phone)
    output = f'Number {phone} is deleted from contact {name}'
    return output

@input_error
def days_to_birth(name: str, *args, **kwargs) -> str:
    '''Remove phone from contact phone numbers'''
    record:Record = address_book.data[name]
    days = record.days_to_birthday()
    output = f'To {name} birthday {days} days'
    return output

@input_error
def upcoming_birth(number: str, *args, **kwargs) -> str:
    '''Shows upcoming birthdays in selected period'''
    if not number:
        return "You should select period in days"
    number = int(number)
    upcoming = address_book.upcoming_birthdays(number)
    if len(upcoming) == 0:
        return "There will be no birthdays in the period you chose"
    return upcoming

@input_error
def remove_contact(name: str, *args, **kwargs) -> str:
    '''Remove contact from address book'''
    address_book.data.pop(name)
    output = f'Contact {name} is deleted'
    return output

def show_all(*args, **kwargs) -> str:
    '''Return message with all contacts'''
    return address_book.show_records()

@input_error
def show_part(*args, **kwargs) -> str:
    '''Return message with n contacts'''
    return next(iterator)

def find_rec(symbols, *args, **kwargs):
    return address_book.find_records(symbols)

def good_bye(*args, **kwargs) -> str:
    '''Return bot goodbye'''
    output = "Good bye"
    address_book.dump_file()
    return output

def save(*args, **kwargs) -> str:
    '''Save data'''
    output = "Changes are saved"
    address_book.dump_file()
    return output

def main_menu(*args, **kwargs) -> str:
    '''Return to the main menu'''
    output = 'Return'
    address_book.dump_file()
    return output

def no_command(*args, **kwargs) -> str:
    '''Answer if there no command'''
    output = 'There no command'
    return output

if __name__ == '__main__':
    print(address_book)