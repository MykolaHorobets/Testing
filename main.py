from fs import Directory, BinaryFile, LogFile, BufferFile, FileSystem
from flask import Flask, jsonify, request, redirect, url_for, abort
import json

app = Flask(__name__)

client = app.test_client()

root = Directory("root", 100)
fs = FileSystem(root)

fs.add_item(Directory('subroot1'), 'root')
fs.add_item(Directory('subroot2'), 'root')
b = BufferFile('buff')
b.push('sdsd')
b.push('dfgkjdfg')
b.push('sdfsdfh')
fs.add_item(BinaryFile('binFile', "dsdfksdbf"), 'root')
fs.add_item(b, 'root')


@app.get("/directory/<path:directory_path>")
def get_directory(directory_path):
    directory = fs.find_directory(directory_path)

    if directory is None:
        return {'error_message': 'Directory not found'}, 400

    return fs.get_items(directory)



@app.get("/bufferfile/<path:file_path>")
def get_buffer_file(file_path):
    buffer_file = fs.find_file(file_path)

    if buffer_file is None or type(buffer_file) is not BufferFile:
        return {'error_message': 'File not found'}, 400

    return fs.get_item(buffer_file)


@app.get("/logfile/<path:file_path>")
def get_log_file(file_path):
    log_file = fs.find_file(file_path)

    if log_file is None or type(log_file) is not LogFile:
        return {'error_message': 'File not found'}, 400

    return fs.get_item(log_file)


@app.get("/binaryfile/<path:file_path>")
def get_binary_file(file_path):
    binary_file = fs.find_file(file_path)

    if binary_file is None or type(binary_file) is not BinaryFile:
        return {'error_message': 'File not found'}, 400

    return fs.get_item(binary_file)


@app.post("/directory/")
def create_directory():
    json = request.get_json()
    directory_path = json.get('directory_path')
    directory_name = json.get('directory_name')
    new_directory = Directory(directory_name)
    is_created = fs.add_item(new_directory, directory_path)

    if is_created:
        return {'success': True}
    else:
        return {'error_message': 'Item with such name already exists'}, 400


@app.post("/bufferfile/")
def create_bufferfile():
    json = request.get_json()
    directory_path = json.get('directory_path')
    buffer_file_name = json.get('file_name')
    new_file = BufferFile(buffer_file_name)
    is_created = fs.add_item(new_file, directory_path)

    if is_created:
        return {'success': True}
    else:
        return {'error_message': 'Item with such name already exists'}, 400


@app.post("/logfile/")
def create_logfile():
    json = request.get_json()
    directory_path = json.get('directory_path')
    binary_file_name = json.get('file_name')
    new_file = LogFile(binary_file_name, "")
    is_created = fs.add_item(new_file, directory_path)

    if is_created:
        return {'success': True}
    else:
        return {'error_message': 'Item with such name already exists'}, 400


@app.post("/binaryfile/")
def create_binaryfile():
    json = request.get_json()
    directory_path = json.get('directory_path')
    binary_file_name = json.get('file_name')
    file_content = json.get('content')
    new_file = BinaryFile(binary_file_name, file_content)
    is_created = fs.add_item(new_file, directory_path)

    if is_created:
        return {'success': True}
    else:
        return {'error_message': 'Item with such name already exists'}, 400


@app.post("/logfile/log")
def log_line_to_file():
    json = request.get_json()
    log_file_path = json.get('log_file_path')
    log_line = json.get('log_line')

    if log_line is None or log_file_path is None:
        return {'error_message': 'Invalid data'}, 400

    log_file = fs.find_file(log_file_path)

    if log_file is None:
        return {'error_message': 'File not found'}, 400

    if type(log_file) is not LogFile:
        return {'error_message': 'File do not supports logging'}, 400

    log_file.append(log_line)
    return {'success': True}


@app.post("/bufferfile/push")
def push_element_to_buffer_file():
    json = request.get_json()
    buffer_file_path = json.get('buffer_file_path')
    element = json.get('push_element')

    if buffer_file_path is None or element is None:
        return {'error_message': 'Invalid data'}, 400

    buffer_file = fs.find_file(buffer_file_path)

    if buffer_file is None:
        return {'error_message': 'File not found'}, 400

    if type(buffer_file) is not BufferFile:
        return {'error_message': 'This operation can not be done with this file'}, 400

    is_pushed = buffer_file.push(element)

    if is_pushed:
        return {'success': True}
    else:
        return {'error_message': 'Element can not be pushed'}, 400


@app.get("/bufferfile/pop/<path:buffer_file_path>")
def pop_element_from_buffer_file(buffer_file_path):
    buffer_file = fs.find_file(buffer_file_path)

    if buffer_file is None:
        return {'error_message': 'File not found'}, 400

    if type(buffer_file) is not BufferFile:
        return {'error_message': 'This operation can not be done with this file'}, 400

    pop_element = buffer_file.pop()

    if pop_element is not None:
        return {'pop_element': pop_element}
    else:
        return {'error_message': 'Buffer file is empty'}, 400


@app.post("/bufferfile/move")
def move_bufferfile():
    json = request.get_json()
    buffer_file_path = json.get('buffer_file_path')
    destination_path = json.get('destination_path')

    buffer_file = fs.find_file(buffer_file_path)

    if buffer_file is None or type(buffer_file) is not BufferFile:
        return {'error_message': 'File not found'}, 400

    is_moved = fs.move_item(buffer_file_path, destination_path)

    if is_moved:
        return {'success': True}
    else:
        return {'error_message': f'File can not be moved to {destination_path}'}, 400


@app.post("/directory/move")
def move_directory():
    json = request.get_json()
    directory_path = json.get('directory_path')
    destination_path = json.get('destination_path')

    directory = fs.find_directory(directory_path)

    if directory is None or type(directory) is not Directory:
        return {'error_message': 'File not found'}, 400

    is_moved = fs.move_item(directory_path, destination_path)

    if is_moved:
        return {'success': True}
    else:
        return {'error_message': f'Directory can not be moved to {destination_path}'}, 400


@app.post("/logfile/move")
def move_logfile():
    json = request.get_json()
    log_file_path = json.get('log_file_path')
    destination_path = json.get('destination_path')

    log_file = fs.find_file(log_file_path)

    if log_file is None or type(log_file) is not LogFile:
        return {'error_message': 'File not found'}, 400

    is_moved = fs.move_item(log_file_path, destination_path)

    if is_moved:
        return {'success': True}
    else:
        return {'error_message': f'File can not be moved to {destination_path}'}, 400


@app.post("/binaryfile/move")
def move_binaryfile():
    json = request.get_json()
    binary_file_path = json.get('binary_file_path')
    destination_path = json.get('destination_path')

    binary_file = fs.find_file(binary_file_path)

    if binary_file is None or type(binary_file) is not BinaryFile:
        return {'error_message': 'File not found'}, 400

    is_moved = fs.move_item(binary_file_path, destination_path)

    if is_moved:
        return {'success': True}
    else:
        return {'error_message': f'File can not be moved to {destination_path}'}, 400


@app.delete("/directory/<path:directory_path>")
def delete_directory(directory_path):
    directory = fs.find_directory(directory_path)

    if directory is None or directory is not Directory:
        return {'error_message': 'Directory not found'}, 400

    is_removed = fs.delete_directory(directory)

    if is_removed:
        return {'success': True}
    else:
        return {'error_message': 'Directory could not be removed'}, 400


@app.delete("/binaryfile/<path:file_path>")
def delete_binaryfile(file_path):
    bin_file = fs.find_file(file_path)

    if bin_file is None or bin_file is not BinaryFile:
        return {'error_message': 'BinaryFile not found'}, 400

    fs.remove_item(bin_file)
    return {'success': True}


@app.delete("/logfile/<path:file_path>")
def delete_logfile(file_path):
    log_file = fs.find_file(file_path)

    if log_file is None or log_file is not LogFile:
        return {'error_message': 'LogFile not found'}, 400

    fs.remove_item(log_file)
    return {'success': True}


@app.delete("/bufferfile/<path:file_path>")
def delete_bufferfile(file_path):
    buffer_file = fs.find_file(file_path)

    if buffer_file is None or buffer_file is not BufferFile:
        return {'error_message': 'LogFile not found'}, 400

    fs.remove_item(buffer_file)
    return {'success': True}


if __name__ == '__main__':
    app.run()
