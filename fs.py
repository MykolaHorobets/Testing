import os

class Directory():

    def create_directory(self, name):
        print("create_directory")

    def create_file(self, name, file_type):
        print("create_file")

    def delete_directory(self, name):
        print("delete_directory")

    def delete_file(self, name):
        print("delete_file")

    def move_file_or_directory(self, old_path, new_parent):
        print("move_file_or_directory")

    def list_files_and_directories(self):
        print("list_files_and_directories")

    def get_node_by_path(self, path):
        print("get_node_by_path")



class File():
    def __init__(self, name, parent=None):
        super().__init__(name, parent)

    def read_file(self):
        print("read_file")

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
        print("push_element")