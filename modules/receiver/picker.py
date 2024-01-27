from . import BaseHandler

from database import PickedSNILS, PickedLastName, PickedFirstName, PickedMiddleName, PickedAddressLocality
from database import PickedDocumentSerial, PickedDocumentNumber, PickedDocumentOrganization
from database import (PickedAddressIndex, PickedAddressRegion, PickedAddressArea, PickedAddressStreet,
                      PickedAddressHouse, PickedAddressBuilding, PickedAddressFlat)
from database import PickedMilitarySubject, PickedMilitaryRank, PickedPersonalNumber

from tools.strings import is_snils_valid, clear_string
from tools.reg_exp import re_full_match


class PickerHandler(BaseHandler):

    def __init__(self, session, class_model, value):
        super().__init__(session, class_model)
        self.value = clear_string(value)  # очищенные данные для модели
        # данные для анализа
        self.is_required = None  # обязательное заполнение поля (по-умолчанию не определено)
        self.reg_exp = None  # регулярное выражение для проверки
        self.min_len = None  # минимальная длина значения
        self.max_len = None  # максимальная длина значения
        self.name = None  # имя поля в кириллице для сообщений об ошибках

    @property
    def length(self):
        return len(self.value)

    def _find_(self):
        # ищем модель по value
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.value == self.value
        ).scalar()
        # если модель найдена
        if model:
            # отмечаем признак существования данных
            self.is_already_exists = True
            # забираем из модели id, created_utc
            self.id = model.id
            self.created_utc = model.created_utc

    def get_model(self):
        """
        Создает модель данных в случае если она еще не присутствует в базе, добавляет ее и синхронизирует состояние
        """
        self._find_()
        if not self.is_already_exists:
            self.model = self._class_name_()
            self.model.id = self.id
            self.model.created_utc = self.created_utc
            self.model.value = self.value
            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        """
        Базовая проверка пикеров на критические ошибки:
        если есть значение, то оно проверяется по регулярному выражению;
        если значения нет, а поле является обязательным;
        проверка на длину значения.
        """
        if self.value:
            if self.reg_exp and not re_full_match(self.reg_exp, self.value):
                self.critical_messages.append('<{}> не соответствует формату {}={}'.format(self.name, self.reg_exp, self.value))
            self.length_check()
        else:
            if self.is_required:
                self.critical_messages.append('обязательное поле <{}> не содержит значения'.format(self.name))

    def length_check(self):
        if self.min_len and self.max_len:
            if self.min_len > self.length or self.length > self.max_len:
                self.critical_messages.append('<{}> недопустимая длина значения {}={} (должно быть {}-{})'.format(
                    self.name, self.value, self.length, self.min_len, self.max_len
                ))


# Обработчики персональных данных


class PickedSNILSHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedSNILS, value)
        self.value = self.value.replace('-', '').replace(' ', '')  # дополнительная очистка
        # данные для анализа
        self.is_required = False
        self.reg_exp = '\d{11}'
        self.name = 'СНИЛС'
        # проверки
        self.check()
        self.get_model()

    def check(self):
        super().check()
        # дополнительные проверки
        if self.value:
            if not self.critical_messages:
                if not is_snils_valid(self.value):
                    self.warning_messages.append('<{}> не прошел проверку контрольного числа ={}'.format(self.name, self.value))
        else:
            self.warning_messages.append('<{}> не содержит значения'.format(self.name))


class PickedLastNameHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedLastName, value)
        # данные для анализа
        self.is_required = True
        self.reg_exp = '[А-Яа-я- ]+'
        self.min_len = 1
        self.max_len = 25
        self.name = 'Фамилия'
        # проверки
        self.check()
        self.get_model()


class PickedFirstNameHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedFirstName, value)
        # данные для анализа
        self.is_required = True
        self.reg_exp = '[А-Яа-я- ]+'
        self.min_len = 1
        self.max_len = 25
        self.name = 'Имя'
        # проверки
        self.check()
        self.get_model()


class PickedMiddleNameHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedMiddleName, value)
        # данные для анализа
        self.is_required = False
        self.reg_exp = '[А-Яа-я- ]+'
        self.min_len = 1
        self.max_len = 25
        self.name = 'Отчество'
        # проверки
        self.check()
        self.get_model()


# Обработчики реквизитов документов


class PickedDocumentSerialHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedDocumentSerial, value)
        self.value = self.value.replace(' ', '')  # дополнительная очистка
        # данные для анализа
        self.is_required = True
        self.reg_exp = '[А-Я0-9]+'
        self.min_len = 1
        self.max_len = 5
        self.name = 'Серия'
        # проверки
        self.check()
        self.get_model()


class PickedDocumentNumberHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedDocumentNumber, value)
        self.value = self.value.replace(' ', '')  # дополнительная очистка
        # данные для анализа
        self.is_required = True
        self.reg_exp = '\d{1,8}'
        self.name = 'Номер'
        # проверки
        self.check()
        self.get_model()


class PickedDocumentOrganizationHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedDocumentOrganization, value)
        # данные для анализа
        self.is_required = False
        self.min_len = 5
        self.max_len = 200
        self.name = 'Орган выдавший документ'
        # проверки
        self.check()
        self.get_model()


# Обработчики составных частей адреса


class PickedAddressIndexHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedAddressIndex, value)
        # данные для анализа
        self.is_required = False
        self.reg_exp = '\d{6}'
        self.name = 'Индекс'
        # проверки
        self.check()
        self.get_model()


class PickedAddressRegionHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedAddressRegion, value)
        # данные для анализа
        self.is_required = False
        self.min_len = 2
        self.max_len = 200
        self.name = 'Регион'
        # проверки
        self.check()
        self.get_model()


class PickedAddressAreaHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedAddressArea, value)
        # данные для анализа
        self.is_required = False
        self.min_len = 2
        self.max_len = 200
        self.name = 'Район'
        # проверки
        self.check()
        self.get_model()


class PickedAddressLocalityHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedAddressLocality, value)
        # данные для анализа
        self.is_required = False
        self.min_len = 2
        self.max_len = 200
        self.name = 'Населенный пункт'
        # проверки
        self.check()
        self.get_model()


class PickedAddressStreetHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedAddressStreet, value)
        # данные для анализа
        self.is_required = False
        self.min_len = 2
        self.max_len = 200
        self.name = 'Улица'
        # проверки
        self.check()
        self.get_model()


class PickedAddressHouseHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedAddressHouse, value)
        # данные для анализа
        self.is_required = False
        self.min_len = 1
        self.max_len = 10
        self.name = 'Дом'
        # проверки
        self.check()
        self.get_model()


class PickedAddressBuildingHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedAddressBuilding, value)
        # данные для анализа
        self.is_required = False
        self.min_len = 1
        self.max_len = 10
        self.name = 'Корпус/Строение'
        # проверки
        self.check()
        self.get_model()


class PickedAddressFlatHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedAddressFlat, value)
        # данные для анализа
        self.is_required = False
        self.min_len = 1
        self.max_len = 10
        self.name = 'Квартира'
        # проверки
        self.check()
        self.get_model()


# Обработчики военной составляющей информации


class PickedPersonalNumberHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedPersonalNumber, value)
        self.value = self.value.replace(' ', '')  # дополнительная очистка
        # данные для анализа
        self.is_required = True
        self.reg_exp = '[А-Я]{1,2}\-\d{6}'
        self.name = 'Личный номер'
        # проверки
        self.check()
        self.get_model()


class PickedMilitaryRankHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedMilitaryRank, value)
        # данные для анализа
        self.is_required = True
        self.name = 'Звание'
        # проверки
        self.check()
        self.get_model()


class PickedMilitarySubjectHandler(PickerHandler):

    def __init__(self, session, value):
        super().__init__(session, PickedMilitarySubject, value)
        # данные для анализа
        self.is_required = True
        self.name = 'Субъект войск'
        # проверки
        self.check()
        self.get_model()
