import os


def remove_file(file_path):
    try:
        os.remove(file_path)
    except OSError as error:
        print(error)
