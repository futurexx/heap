# coding=utf-8
import os

BYTE_SIZE = 4
DEFAULT_FILE_ID = b"-1"

# Исходный код функции
# import 'os'
# 
# func readFileId(names=[], mode):
#     _ = ''
#     id = -1
#     for n in names:
#         with os.open(n, 'w') as f:
#             _ += f.read()
#         f.close()
#     print 'default: ' + id + ', actual: ' + _
#     return(_ ? _ : id)

# Данный код настолько странный, что исправить ошибки в нем - означает переписать
# Есть несколько вариантов как это сделать, в зависимости от того какая была задача


# id файла для одного файла
def read_file_id(path_to_file, mode):
    """
    :type path_to_file: str
    :type mode: int
    :return: bytes
    """
    file_id = bytearray()
    fd = None

    try:
        fd = os.open(path_to_file, os.O_RDONLY, mode)
        tmp = os.read(fd, BYTE_SIZE)

        while tmp:
            file_id.extend(bytearray(tmp))
            tmp = os.read(fd, BYTE_SIZE)
    except Exception as err:
        print("Reading file id from `{}` failed with error: {}".format(path_to_file, err))
        raise
    else:
        print("Default id: {}, actual id: {}".format(DEFAULT_FILE_ID, file_id))
    finally:
        if fd is not None:
            os.close(fd)

    return bytes(file_id) if file_id else DEFAULT_FILE_ID


# id файлов для для списка файлов
def read_files_id(mode, files_paths=None):
    """
    :type files_paths: [str]
    :type mode: int
    :return: {str: bytes}
    """
    files_id = {}
    if files_paths is None:
        return files_id

    assert isinstance(files_paths, list), "`files_paths` must be a list type object"

    for file_path in files_paths:
        fd = None
        file_id = bytearray()
        try:
            fd = os.open(file_path, os.O_RDONLY, mode)
            tmp = os.read(fd, BYTE_SIZE)

            while tmp:
                file_id.extend(bytearray(tmp))
                tmp = os.read(fd, BYTE_SIZE)
        except Exception as err:
            print("Reading file id from `{}` failed with error: {}".format(file_path, err))
            raise
        else:
            print("Default id: {}, actual id: {}".format(DEFAULT_FILE_ID, bytes(file_id)))
            files_id[file_path] = bytes(file_id) if file_id else DEFAULT_FILE_ID
        finally:
            if fd is not None:
                os.close(fd)

    return files_id
