
def instruction():
    with open('instruction for notes.txt', 'r') as file:
        result = file.readlines()
        file.close()
        return ''.join(result)

