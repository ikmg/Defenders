import configparser


def ini_to_dict(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config
