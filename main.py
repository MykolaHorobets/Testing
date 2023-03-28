from fs import Directory, BinaryFile, LogFile, BufferFile, File


def print_node(node, indent=0):
    if isinstance(node, Directory):
        print("  " * indent + "+ " + node.name)
        for child in node.children:
            print_node(child, indent + 1)
    elif isinstance(node, File):
        print("  " * indent + "- " + node.name)



root = Directory("")

dir1 = root.create_directory("dir1")
dir2 = root.create_directory("dir2")


subdir1 = dir1.create_directory("subdir1")
subdir2 = dir1.create_directory("subdir2")
binary_file = BinaryFile("binary_file", dir1)
log_file = LogFile("log_file", subdir1)
buffer_file = BufferFile("buffer_file", subdir2)

subsubdir1 = subdir1.create_directory("subsubdir1")
subsubdir2 = subdir1.create_directory("subsubdir2")
binary_file2 = BinaryFile("binary_file2", subdir1)
log_file2 = LogFile("log_file2", subsubdir1)
buffer_file2 = BufferFile("buffer_file2", subsubdir2)

print_node(root)
