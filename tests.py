from types import NoneType
from fs import Directory, BinaryFile, LogFile, BufferFile


class TestingDirectory:
    fatherDirectory = Directory('fatherDirectory1')

    def test_directory_create(self):
        max_elements = 7
        name = 'dir1'
        directory = Directory(name, max_elements)
        assert directory.DIR_MAX_ELEMS == max_elements
        assert directory.numberOfElements == 0
        assert directory.dirName == name
        assert type(directory.father) is NoneType

    def test_directory_move(self):
        directory = Directory('directory1')
        assert type(directory.father) is NoneType
        directory.move(self.fatherDirectory)
        assert directory.father == self.fatherDirectory

    def test_directory_del(self):
        directory = Directory('directory2')
        del directory
        assert 'directory' not in locals()


class TestingBufferFile:
    fatherDirectory = Directory('fatherDirectory4')
    def test_BufferFileCreate(self):
        name = 'buffer'
        size = 7
        bufferFile = BufferFile(name, size, self.fatherDirectory)
        assert bufferFile.MAX_BUF_FILE_SIZE == size
        assert bufferFile.father == self.fatherDirectory
        assert bufferFile.fileName == name
    def test_BufferFileMove(self):
        name = 'buffer'
        info = 'ekwfjwiojfi'
        bufferFile = BufferFile(name, info)
        assert type(bufferFile.father) is NoneType
        bufferFile.move(self.fatherDirectory)
        assert bufferFile.father == self.fatherDirectory
    def test_BufferFileDel(self):
        bufferFile = BufferFile('buff')
        del bufferFile
        assert 'bufferFile' not in locals()
    def test_BufferFileConsume(self):
        name = 'buffer2'
        size = 7
        bufferFile = BufferFile(name, size)
        element1 = 'e1'
        element2 = 'e2'
        bufferFile.push(element1)
        bufferFile.push(element2)
        assert bufferFile.consume() == element1
        assert bufferFile.consume() == element2
        assert bufferFile.consume() == None


class TestingLogTextFile:
    fatherDirectory = Directory('fatherDirectory3')
    def test_logFileCreate(self):
        name = 'log1'
        info = ''
        logTextFile = LogFile(name, info, self.fatherDirectory)
        assert logTextFile.fileName == name
        assert logTextFile.read() == ''
        assert logTextFile.father == self.fatherDirectory
    def test_logFileMove(self):
        name = 'log2'
        info = ''
        logFile = LogFile(name, info)
        assert type(logFile.father) is NoneType
        logFile.move(self.fatherDirectory)
        assert logFile.father == self.fatherDirectory
    def test_logFileDel(self):
        info = ''
        logTextFile = LogFile('log3', info)
        del logTextFile
        assert 'logTextFile' not in locals()
    def test_logFileAddLine(self):
        name = 'log4'
        info = 'info'
        logFile = LogFile(name, info)
        assert logFile.read() == 'info'
        logFile.appendNewLine('new line')
        assert 'line' in logFile.read()


class TestingBinaryFile:
    fatherDirectory = Directory('fatherDirectory2')

    def test_binary_file_create(self):
        name = 'binary1'
        info = 'kdvjiviufsvvush'
        binary_file = BinaryFile(name, info, self.fatherDirectory)
        assert binary_file.fileName == name
        assert binary_file.info == info
        assert binary_file.read() == info
        assert binary_file.father == self.fatherDirectory

    def test_binary_file_move(self):
        name = 'binary2'
        info = 'kdvjiviufsvvffush'
        binaryFile = BinaryFile(name, info)
        assert type(binaryFile.father) is NoneType
        binaryFile.move(self.fatherDirectory)
        assert binaryFile.father == self.fatherDirectory
    def test_binaryFileDel(self):
        binaryFile = BinaryFile('binary3')
        del binaryFile
        assert 'binaryFile' not in locals()

