import ab_work as ab
import sort

def help(*args, **kwargs):
    return 'Its main menu'

# def address_book(*args, **kwargs):
#     ab.main()

def notes(*args, **kwargs):
    pass

def good_bye(*args, **kwargs):
    return 'good_bye'

def no_command(*args, **kwargs):
    return 'There are no command'

MAIN_COMMANDS = {
    'help': help,
    'address book': ab.main,
    'notes': notes,
    'sort': sort.main,
    'exit': good_bye
}

MAIN_COMMANDS_WORDS = '|'.join(MAIN_COMMANDS)

def main():
    print(help())
    while True:
        user_input = input('Choose points: address book, notes, sort: ')
        command, _ = ab.parser(user_input, MAIN_COMMANDS_WORDS)
        handler = MAIN_COMMANDS.get(command, no_command)
        print(handler())
        if command == good_bye:
            break
    
if __name__ == '__main__':
    main()
    




