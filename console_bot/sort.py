import re
import os
from pathlib import Path
import shutil

import console_bot.ab_work as ab
from console_bot.handlers import no_command, input_error, instruction

SORT_INSTRUCTION = 'instruction for sorter.txt'

extensions={'Зображення':['jpeg', 'png', 'jpg', 'svg'],
           "Відео":['avi', 'mp4', 'mov', 'mkv'],
           "Документи":['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
           "Музика":['mp3', 'ogg', 'wav', 'amr'],
           "Архіви":['zip', 'gz', 'tar'],
           "Невідомі розширення":[]}

def make_translitarate_table() -> dict:
    '''Make translitarate table from cyrillic to latin'''
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", 
        "i", "j", "k", "l", "m", "n", "o", "p", "r", 
        "s", "t", "u","f", "h", "ts", "ch", "sh", "sch", 
        "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
        )
    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    return TRANS

TRANS = make_translitarate_table()

def normalize(word: str, TRANS = TRANS) -> str:
    '''
    Сhecks if the string contains non-Latin letters or non-digits.
    Replace each character in the string using the given translitaration table.
    Then replace all characters in the string by _, exept latin and didgits. 
    '''
    if re.fullmatch('\w+', word, re.A):
        return word

    name_translitarate = word.translate(TRANS)
    normalized_word = re.sub(r'\W', '_', name_translitarate) 
    return normalized_word

def create_dirs(path):
        path = Path(path)
        path.joinpath('Зображення').mkdir(exist_ok=True)
        path.joinpath('Відео').mkdir(exist_ok=True)
        path.joinpath('Документи').mkdir(exist_ok=True)
        path.joinpath('Музика').mkdir(exist_ok=True)
        path.joinpath('Архіви').mkdir(exist_ok=True)
        path.joinpath('Невідомі розширення').mkdir(exist_ok=True)

def get_subfolder_paths(path):
    subfolder_paths = [f.path for f in os.scandir(path) if f.is_dir()]
    return subfolder_paths

def get_file_paths(path):
    file_paths = [f.path for f in os.scandir(path) if not f.is_dir()]
    return file_paths

def sort_files(ls,path):
    file_paths = ls
    ext_list = list(extensions.items())
    lst=[]
    for file_path in file_paths:
        lst.append(file_path)
        extension = file_path.split('.')[-1]
        file_name = file_path.split('\\')[-1]
        normalize_name =file_name.split('.')
        normal= normalize(normalize_name[0])
        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                os.replace(file_path, f'{path}\\{ext_list[dict_key_int][0]}\\{normal}.{extension}')
                lst.remove(file_path)
    for i in lst:
        file_name=i.split('\\')[-1]
        os.replace(i, f'{path}\\Невідомі розширення\\{file_name}')


def get_subfolders(path):
    subfolders = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            subfolders.append(item_path)
            subfolders.extend(get_subfolders(item_path))
    return subfolders

def full_sort(path):
    m= get_subfolders(path)
    for i in m:
        new_path= i
        sort =sort_files(get_file_paths(new_path),path)

def dearchivator(path):
    way = f'{path}\\Архіви'
    j = get_file_paths(way)
    for i in j:
        name = i.split('\\')[-1]
        name=name.split('.')
        (os.mkdir(way + f'\\{normalize(name[0])}'))
        shutil.unpack_archive(i,  f'{way}\\{normalize(name[0])}')
        os.remove(i)

def folder_remover(path):
    list_with_folders = get_subfolders(path)
    list_with_folders.reverse()
    for i in list_with_folders:
        name = i.split('\\')[-1]
        if name not in extensions.keys():
            if len(os.listdir(i))==0:
                os.rmdir(i)

def annotation_file(path):
    message='Result of sorting:\n'
    for i in os.listdir(path):
        name = i.split('\\')[-1]
        message+=f'{name}:\n'
        for k in os.listdir(f'{path}\\{i}'):
                file_name = k.split('\\')[-1]
                message += f'--{file_name}\n'
    with open (f'{path}\\annotation.txt', 'w') as file:
        file.write(message)
    return message

@input_error       
def organize_files(path):
    if not path:
        raise ValueError('You should write path')
                                           
    if os.path.isdir(path):
        create_dirs(path)                          
        sort_files(get_file_paths(path), path)      
        full_sort(path)                               
        dearchivator(path)                       
        folder_remover(path)                                  
        message = annotation_file(path)                           
        return message
    else:
        raise ValueError("Not correct path")

def start(*args, **kwargs):
    return instruction(SORT_INSTRUCTION)

def no_command(*args, **kwargs):
    return 'There are no command like this'

def main_menu(*args, **kwargs) -> str:
    '''Return to the main menu'''
    output = 'Return'
    return output

SORT_COMMANDS = {
    'sort': organize_files,
    'return': main_menu,
    'help': start
}

SORT_COMMANDS_WORDS = '|'.join(SORT_COMMANDS)

def main():
    print(start())
    while True:
        user_input = input('Write your command: ')
        command, data = ab.parser(user_input, SORT_COMMANDS_WORDS)
        handler = SORT_COMMANDS.get(command, no_command)
        output = handler(data)
        print(output)
        if output == 'Return':
            break

if __name__ == '__main__':
    main()