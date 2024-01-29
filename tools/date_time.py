from datetime import datetime, date, timedelta, timezone


def datetime_timezone():
    delta = timedelta(hours=3, minutes=0)
    return datetime.now(timezone.utc) + delta


class ToString:
    """
    Преобразование даты или даты/время в строку
    """

    def __init__(self, value):
        self.value = value

    def convert(self):
        """Конвертер"""
        if isinstance(self.value, datetime):
            return self.value.strftime('%d.%m.%Y %H:%M:%S')
        elif isinstance(self.value, date):
            return self.value.strftime('%d.%m.%Y')
        else:
            return str(self.value)


class ToDate:
    """
    Преобразование значения в дату
    """

    def __init__(self, value):
        self.value = value

    def from_string(self, once=False):
        """Из строки"""
        res = self.rus_format()
        if res:
            return res
        res = self.eng_format()
        if res:
            return res
        res = self.oth_format(once)
        return res

    def rus_format(self):
        """В русском формате"""
        try:
            return datetime.strptime(str(self.value), '%d.%m.%Y').date()
        except:
            return None

    def eng_format(self):
        """В английском формате"""
        try:
            return datetime.strptime(str(self.value), '%Y-%m-%d').date()
        except:
            return None

    def oth_format(self, once=False):
        """В другом формате"""
        if once:
            return None
        else:
            # возможно это строка с датой/временем
            res = ToDateTime(self.value).convert(True)
            return res.date() if res else None

    def convert(self, once=False):
        """Конвертер, параметр once используется чтобы не уйти в рекурсию"""
        if isinstance(self.value, str):
            return self.from_string(once)
        elif isinstance(self.value, datetime):
            return self.value.date()
        elif isinstance(self.value, date):
            return self.value
        else:
            return None


class ToDateTime:
    """
    Преобразование значения в дату/время
    """

    def __init__(self, value):
        self.value = value

    def from_string(self, once=False):
        """Из строки"""
        res = self.eng_full_format()
        if res:
            return res
        res = self.eng_short_format()
        if res:
            return res
        res = self.rus_format()
        if res:
            return res
        res = self.oth_format(once)
        return res

    def eng_full_format(self):
        """В английском формате с милисекундами"""
        try:
            return datetime.strptime(str(self.value), '%Y-%m-%d %H:%M:%S.%f')
        except:
            return None

    def eng_short_format(self):
        """В английском формате без милисекунд"""
        try:
            return datetime.strptime(str(self.value), '%Y-%m-%d %H:%M:%S')
        except:
            return None

    def rus_format(self):
        """В относительно русском формате, но встречается"""
        try:
            return datetime.strptime(str(self.value), '%d-%m-%Y %H:%M:%S')
        except:
            return None

    def oth_format(self, once=False):
        """В другом формате"""
        if once:
            return None
        else:
            # возможно это строка с датой
            res = ToDate(self.value).convert(True)
            return datetime.combine(res, datetime.min.time()) if res else None

    def convert(self, once=False):
        """Конвертер, параметр once используется чтобы не уйти в рекурсию"""
        if isinstance(self.value, str):
            return self.from_string(once)
        elif isinstance(self.value, datetime):
            return self.value
        elif isinstance(self.value, date):
            return datetime.combine(self.value, datetime.min.time())
        else:
            return None


class DateTimeConvert:
    """
    Класс преобразования значения в дату, дату/время
    """

    def __init__(self, value=None):
        self.value = value
        if self.value == None:
            self.value = datetime_timezone()

    @property
    def string(self):
        return ToString(self.value).convert()

    @property
    def date(self):
        return ToDate(self.value).convert()

    @property
    def datetime(self):
        return ToDateTime(self.value).convert()
