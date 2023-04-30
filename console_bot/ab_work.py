import re

import handlers


OPERATIONS = {
    'hello': handlers.hello,
    'add': handlers.adding,
    'change': handlers.changing,
    'phone': handlers.get_phones,
    'show all': handlers.show_all,
    'show part': handlers.show_part,
    'remove contact': handlers.remove_contact,
    'remove phone': handlers.remove_phone,
    'days to birth': handlers.days_to_birth,
    'upcoming birthdays': handlers.upcoming_birth,
    'find': handlers.find_rec,
    'close': handlers.good_bye,
    'good bye': handlers.good_bye,
    'exit':handlers.good_bye, 
    'no command': handlers.no_command
}

COMMAND_WORDS = '|'.join(OPERATIONS)

# add Dima phones: 0979155041 address: 'adhd ahdajsd ashdja a' birthday: 12.12.2000 email: 'cascasc'

def parser(message: str) -> tuple[str|None, str|None, str|None]:
    '''Parse message to command and data'''

    message = message.lstrip()
    command_match = re.search(fr'^({COMMAND_WORDS})\b', message, re.IGNORECASE)
    if command_match:
        command = command_match.group(1)
        data = re.sub(command, '', message).strip()
        command = command.strip().lower()
        return command, data
    return 'no command', ''

def main():
    address_book = handlers.address_book
    print(handlers.hello())
    while True:
        inp = input('Write your command: ')
        command, data  = parser(inp)
        print(data)
        handler = OPERATIONS.get(command, handlers.no_command)
        output = handler(data)
        print(output)
        if output == 'Good bye':
            break
    return address_book

if __name__ == '__main__':
    main()

