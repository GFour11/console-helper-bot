import console_bot.ab_work as ab
from console_bot.handlers import no_command, instruction, show_all
import console_bot.Notes as Notes
import console_bot.sort as sort
from abc import ABC, abstractmethod


MAIN_INSTRUCTION = 'instruction for menu.txt'

class Abstract(ABC):

    @abstractmethod
    def show_contacts(self):
        pass
    @abstractmethod
    def show_notes(self):
        pass
    @abstractmethod
    def help(self):
        pass


class Main(Abstract):
    def show_contacts(self):
        return show_all()
    def show_notes(self):
        return Notes.all([])
    def help(self):
        print("Hello,hello,hello!\n"
              "This bot created by boys from team 6!\n"
              "This bot can replace your phone if you are crazy!Pick 'Address Book' for create your address book.\n"
              "'Sort' - for sort your files.Or 'Notes' for write shopping list or memoirs!\n"
              "Lets go!\n"
              "* for end print 'Exit'")





def good_bye(*args, **kwargs):
    return 'Good bye'

first = Main()


MAIN_COMMANDS = {
    'help': first.help,
    "show contacts": first.show_contacts,
    'show notes': first.show_notes,
    'address book': ab.main,
    'notes': Notes.main,
    'sort': sort.main,
    'exit': good_bye
}


MAIN_COMMANDS_WORDS = '|'.join(MAIN_COMMANDS)

def main():
    print(first.help())
    while True:
        user_input = input('Choose points: address book, notes, sort\n'
                           'Or show contacts, or show notes\n '
                           'for help print help: ')
        command, _ = ab.parser(user_input, MAIN_COMMANDS_WORDS)
        handler = MAIN_COMMANDS.get(command, no_command)
        output = handler()
        if output:
            print(output)
        if output == 'Good bye':
            break


if __name__ == '__main__':
    main()





