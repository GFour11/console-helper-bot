import os
import shutil
import zipfile

import console_bot.ab_work as ab
from console_bot.handlers import input_error, no_command

CATEGORIES = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'videos': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'music': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')
}

@input_error
def organize_files(directory, *args, **kwargs):

    KNOWN_EXTENSIONS = []
    UNKNOWN_EXTENSIONS = []
        
    def normalize(name):
        name = name.translate(str.maketrans('абвгдеёжзийклмнопрстуфхіыэюя', 
                                            'abvgdeejzijklmnoprstufhiyejya'))
        name = ''.join(c if c.isalnum() else '_' for c in name)
        return name


    def move_file(src_path, dst_path, new_name=None):
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        if new_name:
            new_path = os.path.join(dst_path, new_name)
        else:
            new_path = os.path.join(dst_path, os.path.basename(src_path))
        os.rename(src_path, new_path)



    def remove_empty_directories(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                remove_empty_directories(item_path)
                if not os.listdir(item_path):
                    os.rmdir(item_path)


    def extract_archive(archive_path, dst_path):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(dst_path)


    def sort_files(directory):
        nonlocal KNOWN_EXTENSIONS, UNKNOWN_EXTENSIONS
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                sort_files(item_path)
                if not os.listdir(item_path):
                    os.rmdir(item_path)
            else:
                _, ext = os.path.splitext(item)
                ext = ext[1:].upper()
                KNOWN_EXTENSIONS.append(ext)
                for category, extensions in CATEGORIES.items():
                    if ext in extensions:
                        category_path = os.path.join(directory, category)
                        move_file(item_path, category_path)
                        if ext == 'ZIP':
                            extract_archive(os.path.join(category_path, item), category_path)
                    else:
                        UNKNOWN_EXTENSIONS.append(ext)
        remove_empty_directories(directory)
    
    print(directory)
    if not directory:
        directory = input("You dont ente folder name, please write it>>> ")
    if not os.path.isdir(directory):
        raise ValueError("It's not a folder")
    sort_files(directory)
    return 'Done'

def start(*args, **kwargs):
    return 'Here you can sort files'

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
