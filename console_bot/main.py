import console_bot.ab_work as ab
from console_bot.handlers import no_command, instruction
import console_bot.Notes as notes
import console_bot.sort as sort


MAIN_INSTRUCTION = 'instruction for menu.txt'

def help(*args, **kwargs):
    return instruction(MAIN_INSTRUCTION)

def good_bye(*args, **kwargs):
    return 'Good bye'

MAIN_COMMANDS = {
    'help': help,
    'address book': ab.main,
    'notes': notes.main,
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
        output = handler()
        if output:
            print(output)
        if output == 'Good bye':
            break
    
if __name__ == '__main__':
    main()
    




