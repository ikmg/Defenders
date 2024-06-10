import os
import shutil
import hashlib
import platform
import subprocess


# TODO: попробовать pathlib


def get_linux_path(path: str):
    """
    Преобразование пути к формату Linux
    :param path: str
    :return: str
    """
    return path.replace('\\', '/')


def get_windows_path(path: str):
    """
    Преобразование пути к формату Windows
    :param path: str
    :return: str
    """
    return path.replace('/', '\\')


def convert_path(path: str):
    """
    Преобразование пути в зависимости от операционной системы
    :param path: str
    :return: str
    """
    if platform.system() == 'Windows':  # Windows
        return get_windows_path(path)
    else:  # linux variants
        return get_linux_path(path)


def work_directory():
    """
    Путь к рабочему каталогу
    :return: Directory()
    """
    return Directory(os.path.abspath(os.curdir))


class Path:
    """
    Класс пути к объектам операционной системы
    """

    def __init__(self, path: str):
        self.path = os.path.abspath(convert_path(path))

    def __repr__(self):
        return self.path

    @property
    def is_exists(self):
        """
        Проверка существования пути
        :return: bool
        """
        return os.path.exists(self.path)

    @property
    def rel_path(self):
        """
        Относительный путь (без пути к рабочему каталогу)
        :return: str
        """
        return os.path.relpath(self.path, work_directory().path)


class Directory(Path):
    """
    Класс работы с директорией
    """

    def __init__(self, path: str):
        super().__init__(path)
        if not self.is_exists:
            self.create()

    def add_file(self, file_name: str):
        """
        Добавление к пути директории нового элемента
        :param file_name: str
        :return: File()
        """
        return File(os.path.join(self.path, str(file_name)))

    def add_dir(self, dir_name: str):
        """
        Создание дочерней директории
        :param dir_name: str
        :return: Directory()
        """
        return Directory(os.path.join(self.path, str(dir_name)))

    def create(self):
        if not self.is_exists:
            os.mkdir(self.path)

    def open(self):
        """
        Открыть директорию в операционной системе
        :return: None
        """
        if self.is_exists:
            print('открытие директории <{}>'.format(self.rel_path))
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', self.path))
            elif platform.system() == 'Windows':  # Windows
                subprocess.call(('start', "", self.path), shell=True)
            else:  # linux variants
                subprocess.run(['xdg-open', self.path])
        else:
            raise FileNotFoundError('директория не найдена {}'.format(self.path))

    def files_list(self):
        result = []
        children = [self.add_file(i) for i in sorted(os.listdir(self.path))]
        for file in children:
            if os.path.isfile(file.path):
                result.append(file.path)
        return result

    def dirs_list(self):
        result = []
        children = [self.add_file(i) for i in sorted(os.listdir(self.path))]
        for file in children:
            if os.path.isdir(file.path):
                result.append(file.path)
        return result


class File(Path):
    """
    Класс работы с файлом
    """

    def start(self):
        """
        Запуск файла в операционной системе
        :return: None
        """
        if self.is_exists:
            print('открытие файла <{}>'.format(self.rel_path))
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', self.path))
            elif platform.system() == 'Windows':  # Windows
                subprocess.call(('start', "", self.path), shell=True)
            else:  # linux variants
                subprocess.run(['xdg-open', self.path])
        else:
            raise FileNotFoundError('файл не найден {}'.format(self.path))

    def copy(self, destination: str):
        """
        Копирование файла
        :param destination: str
        :return: None
        """
        if self.is_exists:
            print('копирование файла <{}> KB:'.format(self.size_kb))
            print('откуда: <{}>'.format(self.path))
            print('куда: <{}>\n'.format(destination))
            shutil.copyfile(self.path, destination)
        else:
            raise FileNotFoundError('файл не найден {}'.format(self.path))

    def delete(self):
        """
        Удаление файла
        :return: None
        """
        os.remove(self.path)

    def md5(self):
        """
        Хэш-сумма файла
        :return: str
        """
        with open(self.path, 'rb') as f:
            m = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()

    @property
    def dir(self):
        """
        Определение директории файла
        :return: Directory()
        """
        return Directory(os.path.dirname(self.path))

    @property
    def base_name(self):
        """
        Имя файла без пути к нему
        :return: str
        """
        return os.path.basename(self.path)

    @property
    def extension(self):
        """
        Расширение файла
        :return: str
        """
        parts = os.path.splitext(self.base_name)
        if len(parts) == 2:
            return parts[1]
        else:
            return ''

    @property
    def size_b(self):
        return os.path.getsize(self.path)

    @property
    def size_kb(self):
        return round(os.path.getsize(self.path) / 1024, 2)

    @property
    def size_mb(self):
        return round(self.size_kb / 1024, 2)
