from collections import UserDict
from functools import reduce
from datetime import date

class Field():
    '''Common field characters'''
    def __init__(self, value) -> None:
        self.value = value
        pass

    def __eq__(self, __obj: object) -> bool:
        return self.value == __obj.value and type(self) == type(__obj)
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self)

class Name(Field):
    '''Name characters'''
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        else:
            raise ValueError('Cant save contact with empty name')

class Phone(Field):
    '''Phone characters'''
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter 
    def value(self, value: str):
        if value.isdigit():
            self.__value = value
        elif value:
            raise ValueError(f'{value} it\'s not number')

class Birthday(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if type(value) == date:
            self.__value = value

    def __str__(self):
        return self.value.strftime('%B %d')
            
class Record():
    '''Represent record with fields'''
    def __init__(self, name, *phones, birthday=None):
        self.name = name         
        self.phones = [phone for phone in filter(lambda phone: phone.value, phones)]
        self.birthday = birthday

    def __str__(self):
        output = f'name: {self.name.value}'

        phones = self.phones
        if phones: 
            numbers = ', '.join(self.get_numbers())
            output += f' numbers: {numbers}'
        
        if self.birthday:
            birthday = str(self.birthday)
            output += f' birthday: {birthday}'

        return output

    def raise_nonumber(func):
        '''
        Decorator to raise exeption if there are no phone 
        with such number in the phones
        '''
        def inner(self, phone, *args, **kwargs):
            if phone not in self.phones:
                raise ValueError('There are no phone with such number in the phones')
            return func(self, phone, *args, **kwargs)
        return inner
    
    def raise_same_number(func):
        '''
        Decorator to raise exeption if already there is phone 
        with such number in the phones
        '''
        def inner(self, *args, **kwargs):
            phone = args[-1]
            if phone in self.phones:
                raise ValueError('Already there is phone with such number in the phones')
            return func(self, *args, **kwargs)
        return inner
    
    def raise_empty_number(func):
        '''Decorator to raise exeption if phone has empty number'''
        def inner(self, *args, **kwargs):
            for phone in args:
                if not phone.value:
                    raise ValueError('There no number in the command')
            return func(self, *args, **kwargs)
        return inner

    @raise_empty_number
    @raise_same_number
    def add_phone(self, phone: Phone) -> list[Phone]:
        '''Add new phone to phones'''
        self.phones.append(phone)
        return self.phones

    @raise_empty_number
    @raise_nonumber
    def remove_phone(self, phone: Phone) -> list[Phone]:
        '''Remove phone with number from phones'''
        for s_phone in filter(lambda s_phone: s_phone.value == phone.value, self.phones):
            self.phones.remove(s_phone)
        return self.phones
    
    @raise_empty_number
    @raise_nonumber
    @raise_same_number
    def change(self, old_phone: Phone, new_phone: Phone) -> list[Phone]:
        '''Change phone number'''
        for phone in filter(lambda phone: phone == old_phone, self.phones):
            phone.value = new_phone.value
        return self.phones
    
    def get_numbers(self) -> list[str]:
        '''Return list with numbers'''
        numbers = [str(phone) for phone in self.phones]
        return numbers
    
    def days_to_birthday(self):
        '''Return number days to next birthday'''
        today = date.today()
        next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
        if today > next_birthday:
            next_birthday = date(today.year+1, self.birthday.value.month, self.birthday.value.day)
        days = (next_birthday - today).days
        return days

class AdressBook(UserDict):
    '''Represent adress book with records'''

    def add_record(self, record: Record) -> dict[str:Record]:
        '''Add new record to the adress book'''
        key = record.name.value
        self.data[key] = record
        return self.data
    
    def show_records(self) -> str:
        '''Show all records in the adress book data'''
        if not self.data:
            return 'There are no contacts in list'
        output = reduce(lambda s, t: str(s) + '\n' + str(t), 
                        self.data.values(), 'Yor contacts:')
        return output
    
    def find_records(self, symbols: str) -> str:
        '''Find all records with such symbols'''
        output = '\n'.join(
            str(record) for record in self.data.values() 
            if symbols in record.name.value.lower() 
            or symbols in ' '.join(record.get_numbers())
            )
        return output
    
    def __iter__(self):
        return self.iterator()

    def iterator(self, n=2):
        'Return generator that show next n records'
        current = 0
        while current < len(self.data):
            group_number = current // n + 1
            output = reduce(
                lambda s, t: str(s) + '\n' + str(t), 
                list(self.data.values())[current:current+n], 
                f'{group_number} group:'
                )
            yield output
            current += n




