from queue import Queue


class Node:
    def __init__(self, itemName: str) -> None:
        self.__itemName = itemName
        self._isDir = False

    def getName(self) -> str:
        return self.__itemName

    def isDir(self) -> bool:
        return self._isDir


class BinaryFile(Node):
    def __init__(self, fileName: str, fileContent: str) -> None:
        self._content = fileContent
        super().__init__(fileName)

    def read(self) -> str:
        return self._content


class LogFile(BinaryFile):
    def __init__(self, fileName: str, fileContent: str) -> None:
        super().__init__(fileName, fileContent)

    def append(self, line) -> None:
        if len(self._content) == 0:
            self._content += line
        else:
            self._content += f"\n{line}"


class BufferFile(Node):
    def __init__(self, fileName: str) -> None:
        self.__buffer = Queue()
        super().__init__(fileName)

    def push(self, element: str) -> bool:
        if (self.__buffer.qsize() + 1) < 1000:
            self.__buffer.put(element)
            return True
        else:
            return False

    def pop(self) -> str:
        if self.__buffer.empty():
            return None
        else:
            element = self.__buffer.get()
            return element

    def get_elements(self):
        return list(self.__buffer.queue)


class Directory(Node):
    def __init__(self, itemName: str) -> None:
        super().__init__(itemName)
        self.__items = []
        self.__parent = None
        self.__itemsCount = 0
        self._isDir = True

    def addItem(self, item: Node) -> bool:

        if self.getItemByName(item.getName()) != None or item == None:
            return False

        if self.__itemsCount < 10:
            self.__itemsCount += 1
            self.__items.append(item)

            if item.isDir():
                item.setParent(self)

            return True

        return False

    def popItem(self, itemName) -> Node:
        item = self.getItemByName(itemName)
        self.__items.remove(item)
        return item

    def getItemByName(self, name: str) -> Node:
        for item in self.__items:
            if item.getName() == name:
                return item

        return None

    def items(self) -> list:
        return self.__items.copy()

    def setParent(self, newParent):
        self.__parent = newParent

    def getParent(self):
        return self.__parent


class FileSystem:
    def __init__(self) -> None:
        self.__root = Directory("root")

    def getRoot(self) -> Directory:
        return self.__root

    def addItem(self, item, path: str) -> bool:
        if '/' in item.getName():
            return False

        itemDir = self.findDir(path)
        if itemDir == None or item == None:
            return False

        return itemDir.addItem(item)

    def removeItem(self, itemPath: str) -> bool:
        if len(itemPath.split('/')) == 1:
            return False

        item = self.__getItemFromDir(itemPath)
        if item == None:
            return False

        return True

    def moveItem(self, itemPath: str, path: str) -> bool:
        itemDir = self.findDir(path)

        if itemDir == None or len(itemPath.split('/')) == 1:
            return False

        item = self.__getItemFromDir(itemPath)

        if item == None:
            return False

        if itemDir.addItem(item):
            return True
        else:
            pathList = itemPath.split('/')
            pathList.pop()
            fileDirPath = '/'.join(pathList)
            fileDir = self.findDir(fileDirPath)
            fileDir.addItem(item)
            return False

    def __getItemFromDir(self, itemPath: str) -> Node:
        pathList = itemPath.split('/')
        itemName = pathList.pop()
        itemDirPath = '/'.join(pathList)
        itemDir = self.findDir(itemDirPath)
        item = itemDir.popItem(itemName)
        return item

    def findDir(self, path: str) -> Directory:
        folders = path.split('/')
        folders = list(filter(lambda item: item != '', folders))

        if len(folders) == 0:
            return None

        rootName = folders.pop(0)

        if self.__root.getName() != rootName:
            return None

        searchedDir = self.__root
        for folder in folders:
            subDir = searchedDir.getItemByName(folder)

            if subDir == None or not subDir.isDir():
                return None
            searchedDir = subDir

        return searchedDir

    def findFile(self, filePath: str):
        if filePath is None:
            return None

        pathList = filePath.split('/')
        fileName = pathList.pop()
        fileDirPath = '/'.join(pathList)
        fileDir = self.findDir(fileDirPath)

        if fileDir is None:
            return None

        return fileDir.getItemByName(fileName)


def get_item_type(item) -> str:
    if item.isDir():
        return 'Directory'

    if type(item) is LogFile:
        return 'LogFile'

    if type(item) is BinaryFile:
        return 'BinaryFile'

    if type(item) is BufferFile:
        return 'BufferFile'

    return 'Unknown'


def get_file_content(file_type: str, file: Node):
    if file_type == 'BinaryFile' or file_type == 'LogFile':
        return file.read()

    if file_type == 'BufferFile':
        return file.get_elements()

    return ""


def get_item_info(item: Node):
    return {'name': item.getName(), 'isDir': item.isDir(), 'itemType': get_item_type(item)}


def get_items(items: list):
    result = []
    for item in items:
        result.append(get_item_info(item))

    return result


def get_file_data(file):
    file_data = get_item_info(file)
    file_content = get_file_content(file_data['itemType'], file)
    file_data['file_content'] = file_content
    return file_data