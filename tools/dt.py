from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta, timezone


class Base(ABC):
    """
    Базовый класс конвертации
    """

    def __init__(self, value: any):
        self.value = value

    def __repr__(self):
        return self.value

    @abstractmethod
    def datetime(self):
        """
        Преобразование self.value к datetime
        :return: datetime | None
        """
        pass

    @abstractmethod
    def date(self):
        """
        Преобразование self.value к date
        :return: date | None
        """
        pass

    @abstractmethod
    def dstring(self):
        """
        Преобразование self.value к str
        :return: str | None
        """
        pass

    @abstractmethod
    def dtstring(self):
        """
        Преобразование self.value к str
        :return: str | None
        """
        pass


class DateTime(Base):
    """
    Конвертация даты/времени
    """

    def __init__(self, value: datetime):
        super().__init__(value)

    def datetime(self) -> datetime:
        return self.value

    def date(self) -> date:
        return self.value.date()

    def dstring(self) -> str:
        return self.value.strftime('%d.%m.%Y')

    def dtstring(self) -> str:
        return self.value.strftime('%d.%m.%Y %H:%M:%S')


class Date(Base):
    """
    Конвертация даты
    """

    def __init__(self, value: date):
        super().__init__(value)

    def datetime(self) -> datetime:
        return datetime.combine(self.value, datetime.min.time())

    def date(self) -> date:
        return self.value

    def dstring(self) -> str:
        return self.value.strftime('%d.%m.%Y')

    def dtstring(self) -> str:
        return self.value.strftime('%d.%m.%Y 00:00:00')


def convert(value):
    # попытка преобразовать строку в дату/время
    dt_variants = [
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        '%d.%m.%Y %H:%M:%S',
        '%Y%m%d-%H%M%S'
    ]
    for variant in dt_variants:
        try:
            dt = datetime.strptime(value, variant)
            # print('DATETIME success mask', variant)
            return DateTime(dt)
        except Exception:
            pass
    # попытка преобразовать строку в дату
    d_variants = [
        '%d.%m.%Y',
        '%d/%m/%Y',
        '%Y/%m/%d',
        '%Y-%m-%d',
        '%d.%m.%y'
    ]
    for variant in d_variants:
        try:
            dt = datetime.strptime(value, variant)
            # print('DATE success mask', variant)
            return Date(dt.date())
        except Exception:
            pass
    # если ничего не получилось
    return None


class DTConvert(Base):

    def __init__(self, value: any = None):
        super().__init__(value)
        if self.value:
            if isinstance(self.value, datetime):
                self._model_ = DateTime(self.value)
            elif isinstance(self.value, date):
                self._model_ = Date(self.value)
            elif isinstance(self.value, str):
                self._model_ = convert(self.value)
            else:
                self._model_ = None
        else:
            delta = timedelta(hours=3, minutes=0)
            self._model_ = DateTime(datetime.now(timezone.utc) + delta)

    @property
    def datetime(self):
        return self._model_.datetime() if self._model_ else None

    @property
    def date(self):
        return self._model_.date() if self._model_ else None

    @property
    def dstring(self):
        return self._model_.dstring() if self._model_ else None

    @property
    def dtstring(self):
        return self._model_.dtstring() if self._model_ else None
