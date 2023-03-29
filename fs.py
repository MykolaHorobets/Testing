import json


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
        self.file_name = file_name
        self.info = info
        self.father = father
        self.id = id

    def __delete__(self):
        print('Destructor called, ' + self.file_name + 'was deleted')
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
        self.file_name = file_name
        self.father = father
        self.info = info

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

    def read(self):
        return self.info

    def append(self, new_line):
        self.info += new_line
        self.info += '\n'


class BufferFile:
    def __init__(self, file_name, max_size=0, father=None):
        self.file_name = file_name
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


class FileSystem:
    def __init__(self, root):
        self.root = Directory("root")

    def find_item(self, item_name, current_dir=None):
        if current_dir is None:
            current_dir = self.root
        for item in current_dir.listOfFiles:
            if item.file_name == item_name:
                return item
            if isinstance(item, Directory):
                found_item = self.find_item(item_name, item)
                if found_item:
                    return found_item
        return None

    def find_directory(self, path):
        if path == "root":
            return self.root

        path_parts = path.split('/')
        current_dir = self.root
        for part in path_parts:
            if part == '':
                continue
            found = False
            for item in current_dir.listOfFiles:
                if isinstance(item, Directory) and item.dirName == part:
                    current_dir = item
                    found = True
                    break
            if not found:
                print(f"Path '{path}' not found.")
                return None
        return current_dir

    def get_item(self, item_name):
        item = self.find_item(item_name)
        if item:
            if isinstance(item, (BinaryFile, LogFile, BufferFile)):
                item_data = {
                    'name': item.file_name,
                    'info': item.read()
                }
            elif isinstance(item, Directory):
                item_data = {
                    'name': item.dirName,
                    'contents': json.loads(self.get_items(item))
                }
            else:
                print(f"Item '{item_name}' not found.")
                return None
            return json.dumps(item_data, indent=2)
        else:
            print(f"Item '{item_name}' not found.")
            return None

    def remove_item(self, item_name, current_dir=None):
        if current_dir is None:
            current_dir = self.root
        for i, item in enumerate(current_dir.listOfFiles):
            if item.file_name == item_name:
                current_dir.listOfFiles.pop(i)
                current_dir.numberOfElements -= 1
                item.father = None
                return
            if isinstance(item, Directory):
                self.remove_item(item_name, item)
        print(f"Item '{item_name}' not found.")

    def move_item(self, current_path, destination_path):
        item = self.get_item_from_directory(current_path)
        if item:
            target_dir = self.find_directory(destination_path)
            if target_dir:
                if target_dir.numberOfElements < target_dir.DIR_MAX_ELEMS or target_dir.DIR_MAX_ELEMS == 0:
                    item.father.listOfFiles.remove(item)
                    item.father.numberOfElements -= 1
                    target_dir.listOfFiles.append(item)
                    target_dir.numberOfElements += 1
                    item.father = target_dir
                    print(f"Item '{item.file_name}' moved from '{current_path}' to '{destination_path}'.")
                else:
                    print(f"Destination directory '{target_dir.dirName}' is full. Cannot move '{item.file_name}'.")
            else:
                print(f"Destination directory '{destination_path}' not found.")
        else:
            print(f"Item '{current_path}' not found.")

    def get_item_from_directory(self, path):
        path_parts = path.split('/')
        item_name = path_parts.pop()
        dir_path = '/'.join(path_parts)
        directory = self.find_directory(dir_path)
        if directory:
            for item in directory.listOfFiles:
                if item.file_name == item_name:
                    return item
            print(f"Item '{item_name}' not found in directory '{directory.dirName}'.")
            return None
        else:
            print(f"Directory '{dir_path}' not found.")
            return None

    def get_items(self, current_dir=None):
        if current_dir is None:
            current_dir = self.root
        items = []
        for item in current_dir.listOfFiles:
            if isinstance(item, Directory):
                item_type = 'Directory'
                item_name = item.dirName
            elif isinstance(item, (BinaryFile, LogFile, BufferFile)):
                item_type = 'File'
                item_name = item.file_name
            else:
                continue

            items.append({
                'name': item_name,
                'type': item_type
            })

        return json.dumps(items, indent=2)

    def find_file(self, path):
        path_parts = path.split('/')
        current_dir = self.root
        for part in path_parts:
            if part == '':
                continue
            found = False
            for item in current_dir.listOfFiles:
                if isinstance(item, Directory) and item.dirName == part:
                    current_dir = item
                    found = True
                    break
                elif item.file_name == part:
                    return item
            if not found:
                print(f"Path '{path}' not found.")
                return None
        print(f"Path '{path}' not found.")
        return None

    def delete_directory(self, path):
        directory = self.find_directory(path)
        if directory:
            if directory.father is not None:
                directory.father.listOfFiles.remove(directory)
                directory.father.numberOfElements -= 1
                directory.father = None
                del directory
                print(f"Directory '{path}' deleted.")
            else:
                print("Cannot delete root directory.")
        else:
            print(f"Directory '{path}' not found.")

    def add_item(self, item, path):
        target_dir = self.find_directory(path)
        if target_dir:
            if isinstance(item, Directory):
                item_name = item.dirName
            else:
                item_name = item.file_name

            if target_dir.numberOfElements < target_dir.DIR_MAX_ELEMS or target_dir.DIR_MAX_ELEMS == 0:
                target_dir.listOfFiles.append(item)
                target_dir.numberOfElements += 1
                item.father = target_dir

                print(f"Item '{item_name}' added to '{path}'.")
            else:
                print(f"Directory '{target_dir.dirName}' is full. Cannot add '{item_name}'.")
        else:
            print(f"Directory '{path}' not found.")


