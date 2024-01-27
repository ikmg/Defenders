import pyexcel
from abc import abstractmethod

from tools.fs import File
from tools.date_and_time import datetime_timezone


class WorkBook:
    """
    Класс загрузки файлов электронных таблиц ODS, XLS
    """

    def __init__(self, **keywords):
        """
        Конструктор класса
        :param debug_mode: bool
        """
        self._debug_mode_ = keywords['debug_mode']  # режим отладки
        self.file = File(keywords['file_path'])  # путь к файлу книги
        self.is_correct = False

        self._workbook_ = None

        self._log_ = []  # лог операций с книгой
        self._data_ = None  # данные в книге

    def _set_null_(self):
        """
        Обнуляет аттрибуты класса
        :return: nothing
        """
        self._log_ = []
        self._data_ = None
        self.file = None
        self.is_correct = False

    def _add_to_log_(self, text):
        """
        Добавляет в лог операций сообщение с временной меткой и входящим текстом
        :param text: str
        :return: nothing
        """
        record = [
            datetime_timezone().strftime('%d.%m.%Y %H:%M:%S.%f'),
            text
        ]
        self._log_.append(record)
        if self._debug_mode_:
            print('<Workbook event>', ': '.join(record))

    @property
    def filename(self):
        """
        Имя файла без пути
        :return: str | None
        """
        if self.file:
            return self.file.base_name
        else:
            self._add_to_log_('Ошибка чтения файла: невозможно определить имя файла, отсутствует путь к файлу')
            return None

    @property
    def worksheets_list(self):
        """
        Список листов в книге
        :return: list
        """
        if self._data_:
            return self._data_.sheet_names()
        else:
            self._add_to_log_('Ошибка чтения файла: невозможно определить список листов в книге')
            return []

    @property
    def log(self):
        """
        Лог операций
        :return: list
        """
        result = []
        for record in self._log_:
            result.append(': '.join(record))
        return '\n'.join(result)

    def print_log(self):
        """
        Печать лога
        :return: nothing
        """
        print('WORKBOOK LOG:')
        for record in self.log:
            print(record)

    def load_workbook(self, file_path):
        """
        Загрузка данных книги из пути к файлу
        :param file_path: str
        :return: nothing
        """
        # self._set_null_()
        self.file = File(file_path)
        try:
            self._add_to_log_('Чтение книги: <{}>'.format(self.file))
            self._data_ = pyexcel.get_book(file_name=self.file)
            self._add_to_log_('Чтение книги: данные из <{}> загружены'.format(self.filename))
            self.is_correct = self.check()
        except Exception as e:
            self._add_to_log_('Ошибка чтения книги: не удалось открыть <{}> ({})'.format(self.filename, str(e)))

    @abstractmethod
    def check(self):
        """
        Абстрактный метод проверки структуры книги
        :return: bool
        """
        pass

    def get_worksheet_data(self, worksheet_name):
        """
        Получение данных из листа книги по его имени
        :param worksheet_name: str
        :return: list
        """
        self._add_to_log_('Чтение листа: <{}> запрос содержимого'.format(worksheet_name))
        if worksheet_name in self.worksheets_list:
            result = self._data_.sheet_by_name(worksheet_name).array
            self._add_to_log_('Чтение листа: <{}> содержимое получено'.format(worksheet_name))
            return result
        else:
            self._add_to_log_('Ошибка чтения листа: лист <{}> отсутствует в книге <{}>'.format(worksheet_name, self.filename))
            return None
