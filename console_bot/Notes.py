from collections import UserDict
import re
import pickle
import os


class HashTags:
    def __init__(self, hashtags):
        self.value = hashtags

class NoteRecord:
    def __init__(self, record, hashtags: HashTags = None):
        self.record = record
        if hashtags:
            self.hashtags = hashtags
        else:
            self.hashtags = None

class Notes(UserDict):
    def add_note(self, note_record: NoteRecord):
        theme = note_record.record.split(' ')
        key =[]
        for i in range(1):
            key.append(theme[i])
        self.data[' '.join(key)] = note_record
        return self.data

    def edit_note(self, note_key, new_record):
        if note_key in self.data:
            self.data[note_key].record = new_record
        else:
            raise KeyError(f'No note found with key "{note_key}"')

    def remove_note(self, note_key):
        if note_key in self.data:
            del self.data[note_key]
        else:
            raise KeyError(f'No note found with key "{note_key}"')

    def save_in_file(self):
        if os.path.isfile('notes.bin'):
            with open('notes.bin', 'wb') as fh:
                pickle.dump(self, fh)
        else:
            with open('notes.bin', 'wb') as fh:
                pickle.dump(self, fh)


    @staticmethod
    def open_from_file():
        if os.path.isfile('notes.bin'):
            with open('notes.bin', 'rb') as fh:
                return pickle.load(fh)
        else:
            return Notes()






notes = Notes.open_from_file()






def add(result):
    if len(result) == 3:
        hashtags = result[2]
        record = NoteRecord(result[1],hashtags)
        notes.add_note(record)
    else:
        record = NoteRecord(result[1])
        notes.add_note(record)


def all(result):
    for k, v in notes.items():
        print(f'Theme:{k},\n {v.record}')


def change(result):
    theme = result[1].split(' ')
    key = theme[0]
    note = " ".join(theme[1:])
    notes.edit_note(key, note)
    notes.save_in_file()

def remove(result):
    key = result[1]
    notes.remove_note(key)
    notes.save_in_file()


"""Сюди записуйте як ви хочете щоб команда викликалась( яким словом) і через : назву функції """
commands_dict ={'add': add, 'all': all, 'change': change, 'remove': remove}

"""Зміст парсера такий: якщо він знаходить в тексті інтпута слово, що є командою, він повертає список у якому йде[команда, текст нотатка,
 список хештегів якщо вони присунті(тобто список в списку)]. якщо комади немає поверне None """
def message_parser(text):
    command=None
    note = None
    hashtags = None
    str=text.lower()
    for i in commands_dict:
        res = re.findall(i,str)
        if len(res)>0:
            command = i
            break
    info = []
    flag = False
    for i in str.split():
        if flag:
            info.append(i)
        elif i == command:
            flag = True
    if len(info)>0:
        note=' '.join(info)
    if note:
        mess = note.split(' ')
        tags =[]
        for i in mess:
            if i.startswith('#'):
                tags.append(i)
        if len(tags)>0:
            hashtags = tags
    if hashtags:
        return [command, note, hashtags]
    else:
        if command:
            return [command, note]


def main():
    while True:
        text = input('>>>')
        if text == 'exit':
            notes.save_in_file()
            print('bye')
            break
        res = message_parser(text)
        if res:
            if res[0] in commands_dict:
                commands_dict[res[0]](res)
        else:
            print("can't see a command")

if __name__ == '__main__':
    main()