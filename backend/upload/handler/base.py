from abc import ABC, abstractmethod
from uuid import uuid4

from tools import DTConvert


class BaseHandler(ABC):
    """
    Абстрактный базовый обработчик.
    Предназначен для обработки входных данных и построения (получения) модели.
    """

    def __init__(self, session, class_model):
        self._session_ = session
        self._class_name_ = class_model
        self.id = str(uuid4())  # идентификатор для модели данных по-умолчанию
        self.created_utc = DTConvert().datetime   # временная метка создания данных для модели по-умолчанию
        self.model = None  # модель данных если данные еще не присутствуют в базе данных
        self.is_already_exists = False  # признак того, что данные уже присутствуют в базе данных
        self.warning_messages = []  # список предупреждений
        self.critical_messages = []  # список критических ошибок

    @abstractmethod
    def _find_(self):
        """
        Абстрактный метод поиска уже имеющейся модели.
        Устанавливает значение атрибута is_already_exists
        """
        pass

    @abstractmethod
    def get_model(self):
        """
        Абстрактный метод получения модели.
        Должен возвращать объект класса _class_name_ в случае если not is_already_exists, иначе None
        """
        pass

    @abstractmethod
    def check(self):
        """
        Абстрактный метод проверки входных данных.
        Формирует список предупреждений и критических ошибок.
        """
        pass

    @property
    def warning(self):
        """Объединяет список предупреждений в строку"""
        return ', '.join(self.warning_messages) if self.warning_messages else ''

    @property
    def critical(self):
        """Объединяет список критических ошибок в строку"""
        return ', '.join(self.critical_messages) if self.critical_messages else ''


class BaseKeeperRecordHandler(BaseHandler):

    def __init__(self, session, class_model, **keywords):
        super().__init__(session, class_model)
        self.keep_row_num = keywords['keep_row_num']
        self.file_row_num = keywords['file_row_num']

    @abstractmethod
    def _find_(self):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def check(self):
        pass


class BaseKeeperFileHandler(BaseHandler):

    def __init__(self, session, class_model):
        super().__init__(session, class_model)
        # self.workbook = None
        # self.original_file_path = None
        # self.file_path = None
        # self.file_relpath = None

    @abstractmethod
    def _find_(self):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def check(self):
        pass
