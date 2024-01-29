import configparser

from tools import File


def dict_from_ini(file_path):
    file = File(file_path)
    if not file.is_exists:
        raise FileNotFoundError('файл <{}> не существует'.format(file.path))
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
