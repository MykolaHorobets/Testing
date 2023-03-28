import os

DIR_MAX_ELEMS = 10
MAX_BUF_FILE_SIZE = 5


class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def get_full_path(self):
        if self.parent is None:
            return self.name
        else:
            return os.path.join(self.parent.get_full_path(), self.name)


class Directory(Node):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.children = []

    def create_directory(self, name):
        if len(self.children) >= DIR_MAX_ELEMS:
            return "Directory is full."
        else:
            dir = Directory(name, self)
            self.children.append(dir)
            return dir

    def create_file(self, name, file_type):
        if len(self.children) >= DIR_MAX_ELEMS:
            return "Directory is full."
        else:
            if file_type == "Binary":
                file = BinaryFile(name, self)
            elif file_type == "Log":
                file = LogFile(name, self)
            elif file_type == "Buffer":
                file = BufferFile(name, self)
            self.children.append(file)
            return "File created."

    def delete_directory(self, name):
        for child in self.children:
            if isinstance(child, Directory) and child.name == name:
                self.children.remove(child)
                return "Directory deleted."
        return "Directory not found."

    def delete_file(self, name):
        for child in self.children:
            if isinstance(child, File) and child.name == name:
                self.children.remove(child)
                return "File deleted."
        return "File not found."

    def move_file_or_directory(self, old_path, new_parent):

        node = self.get_node_by_path(old_path)
        if node is None:
            return "Node not found."

        node.parent.children.remove(node)

        node.parent = new_parent
        new_parent.children.append(node)

        return "Node moved."

    def list_files_and_directories(self):
        return [child.name for child in self.children]

    def get_node_by_path(self, path):
        if path == self.name:
            return self

        for child in self.children:
            if isinstance(child, Directory):
                node = child.get_node_by_path(path)
                if node is not None:
                    return node
            elif child.name == path:
                return child

        return None


class File(Node):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

    def read_file(self):
        pass


class BinaryFile(File):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

    def read_file(self):
        return "Binary file content."


class LogFile(File):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.content = []

    def read_file(self):
        return "\n".join(self.content)

    def append_line(self, line):
        self.content.append(line)


class BufferFile(File):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.buffer = []

    def push_element(self, element):
        if len(self.buffer) < MAX_BUF_FILE_SIZE:
            self.buffer.append(element)
