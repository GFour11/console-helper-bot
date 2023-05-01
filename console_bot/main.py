import console_bot.ab_work as ab
import console_bot.notes as notes
import console_bot.sort as sort

def help(*args, **kwargs):
    return 'Its main menu'

def good_bye(*args, **kwargs):
    return 'Good bye'

def no_command(*args, **kwargs):
    return 'There are no command'
def instruction(path):
    with open(path, 'r') as file:
        result = file.readlines()
        file.close()
        return ''.join(result)

MAIN_COMMANDS = {
    'help': help,
    'address book': ab.main,
    'notes': notes.main,
    'sort': sort.main,
    'exit': good_bye
}

MAIN_COMMANDS_WORDS = '|'.join(MAIN_COMMANDS)

def main():
    print(instruction('instruction for menu.txt'))
    while True:
        user_input = input('Choose points: address book, notes, sort: ')
        command, _ = ab.parser(user_input, MAIN_COMMANDS_WORDS)
        handler = MAIN_COMMANDS.get(command, no_command)
        output = handler()
        print(output)
        if output == 'Good bye':
            break
    
if __name__ == '__main__':
    main()
    




