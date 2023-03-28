class Directory:
    def __init__(self, dir_name, max_elements=0, father=None):
        self.father = father
        if self.father is not None:
            self.father.numberOfElements += 1
            father.listOfFiles.append(self)
        self.dirName = dir_name
        self.DIR_MAX_ELEMS = max_elements
        self.numberOfElements = 0
        self.listOfFiles = []

    def __delete__(self):
        print('Destructor called, ' + self.dirName + 'was deleted')
        return

    def list_elements(self):
        result = self.dirName + ':('
        for item in self.listOfFiles:
            if type(item) is Directory:
                # result += self.dirName #+ '\n'
                result += item.list_elements()
            else:
                result += item.file_name + ', ' + '\n'
        result += ') '
        return result

    def move(self, path):
        if path.numberOfElements >= path.DIR_MAX_ELEMS + 1:
            print('This directory is full, try other')
            return
        if self.father is not None:
            self.father.numberOfElements -= 1
            self.father.listOfFiles.pop(self.father.listOfFiles.index(self))
        self.father = path
        self.father.listOfFiles.append(self)
        self.father.numberOfElements += 1
        return


class BinaryFile:
    def __init__(self, id, file_name, info=None, father=None):
        self.fileName = file_name
        self.info = info
        self.father = father
        self.id = id

    def __delete__(self):
        print('Destructor called, ' + self.fileName + 'was deleted')
        return

    def move(self, path):
        if path.numberOfElements >= path.DIR_MAX_ELEMS + 1:
            print('This directory is full, try other')
            return
        self.father = path
        self.father.listOfFiles.append(self)
        self.father.numberOfElements += 1
        return

    def read(self):
        return self.info


class LogFile:
    def __init__(self, file_name, info, father=None):
        self.fileName = file_name
        self.father = father
        self.info = info

    def __delete__(self):
        print('Destructor called', + self.fileName + 'was deleted')
        return

    def move(self, path):
        if path.numberOfElements >= path.DIR_MAX_ELEMS + 1:
            print('This directory is full, try other')
            return
        self.father = path
        self.father.listOfFiles.append(self)
        self.father.numberOfElements += 1
        return

    def read(self):
        return self.info

    def append(self, new_line):
        self.info += new_line
        self.info += '\n'


class BufferFile:
    def __init__(self, file_name, max_size=0, father=None):
        self.fileName = file_name
        self.father = father
        self.info = []
        self.MAX_BUF_FILE_SIZE = max_size

    def __delete__(self):
        print('Destructor called', + self.file_name + 'was deleted')
        return

    def move(self, path):
        if path.numberOfElements >= path.DIR_MAX_ELEMS + 1:
            print('This directory is full, try other')
            return
        self.father = path
        self.father.listOfFiles.append(self)
        self.father.numberOfElements += 1
        return

    def push(self, item):
        if len(self.info) >= self.MAX_BUF_FILE_SIZE:
            print('This file is full with items')
            return
        self.info.append(item)

    def consume(self):
        if len(self.info) >= 1:
            temp = self.info[0]
            self.info.pop(0)
            return temp
        return None
