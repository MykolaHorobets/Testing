from fs import Directory, BinaryFile, LogFile, BufferFile

print('this is lab1')
root = Directory('root', 100)
directory1 = Directory('child1', 20, root)
directory2 = Directory('child2', 3, root)
directory3 = Directory('chchild', 10, directory1)

binaryFile1 = BinaryFile('binFile1', 'info1', root)
binaryFile2 = BinaryFile('binFile2', 'info2', directory3)
print(binaryFile2.read())

logTextFile1 = LogFile('log1', 'loginfo1', root)
logTextFile2 = LogFile('log2', 'This is', directory2)
logTextFile2.append(' QA lab1')
print(logTextFile2.read())

bufferFile1 = BufferFile('buf1', 5, root)
bufferFile2 = BufferFile('buf2', 3, directory1)
print(type(root.listOfFiles))
print("-----------------------------------------------------------------------------------------")
print(root.list_elements())
