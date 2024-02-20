from datetime import timedelta
from uuid import uuid4

from database import (LinkedPerson, LinkedDocument, LinkedDocumentVBD, LinkedAddress,
                      LinkedOrderFIO, LinkedOrderPerson, LinkedOrderPersonPeriod, LinkedDefender, EskkGender, EskkDocumentType)

from .base import BaseHandler
from .picker import PickedSNILSHandler, PickedLastNameHandler, PickedFirstNameHandler, PickedMiddleNameHandler
from .picker import PickedDocumentSerialHandler, PickedDocumentNumberHandler, PickedDocumentOrganizationHandler
from .picker import (PickedAddressIndexHandler, PickedAddressRegionHandler, PickedAddressAreaHandler, PickedAddressLocalityHandler,
               PickedAddressStreetHandler, PickedAddressHouseHandler, PickedAddressBuildingHandler, PickedAddressFlatHandler)
from .picker import PickedMilitaryRankHandler, PickedPersonalNumberHandler, PickedMilitarySubjectHandler

from tools import DTConvert
from tools.strings import clear_string, get_fio_list
from tools.reg_exp import re_full_match


class LinkedPersonHandler(BaseHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, LinkedPerson)
        self.picked_snils = PickedSNILSHandler(session, keywords['snils'])
        self.picked_last_name = PickedLastNameHandler(session, keywords['last_name'])
        self.picked_first_name = PickedFirstNameHandler(session, keywords['first_name'])
        self.picked_middle_name = PickedMiddleNameHandler(session, keywords['middle_name'])
        self.eskk_gender_id = clear_string(keywords['eskk_gender_id'])
        self.birthday = clear_string(keywords['birthday'])
        self.get_model()
        self.check()

    @property
    def birthday_date(self):
        return DTConvert(self.birthday).date  # должна быть строка

    def is_gender_exists(self):
        model = self._session_.query(EskkGender).filter(
            EskkGender.id == self.eskk_gender_id
        ).scalar()
        if model:
            return True
        else:
            self.critical_messages.append('<Пол> содержит недопустимое значение ={}'.format(self.eskk_gender_id))
            self.eskk_gender_id = '0'
            return False

    def age(self, years):
        control_date = self.birthday_date
        if control_date:
            if control_date.month == 2 and control_date.day == 29:
                control_date += timedelta(days=1)
                return control_date.replace(year=control_date.year + years)
            else:
                return control_date.replace(year=control_date.year + years)
        else:
            return None

    def _find_(self):
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.picked_snils_id == self.picked_snils.id,
            self._class_name_.picked_last_name_id == self.picked_last_name.id,
            self._class_name_.picked_first_name_id == self.picked_first_name.id,
            self._class_name_.picked_middle_name_id == self.picked_middle_name.id,
            self._class_name_.eskk_gender_id == self.eskk_gender_id,
            self._class_name_.birthday == self.birthday
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc

    def get_model(self):
        self.is_gender_exists()
        self._find_()
        if not self.is_already_exists:
            self.model = self._class_name_()
            # self.model = LinkedPerson()
            self.model.id = self.id
            self.model.created_utc = self.created_utc

            self.model.picked_snils_id = self.picked_snils.id
            if self.picked_snils.model:
                self.model.picked_snils = self.picked_snils.model

            self.model.picked_last_name_id = self.picked_last_name.id
            if self.picked_last_name.model:
                self.model.picked_last_name = self.picked_last_name.model

            self.model.picked_first_name_id = self.picked_first_name.id
            if self.picked_first_name.model:
                self.model.picked_first_name = self.picked_first_name.model

            self.model.picked_middle_name_id = self.picked_middle_name.id
            if self.picked_middle_name.model:
                self.model.picked_middle_name = self.picked_middle_name.model

            self.model.eskk_gender_id = self.eskk_gender_id
            self.model.birthday = self.birthday

            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        # проверка даты рождения
        if self.birthday:
            if self.birthday_date:
                if self.age(18) > DTConvert().date:
                    self.critical_messages.append('<Персона> должна быть старше 18 лет ={}'.format(self.birthday))
            else:
                self.critical_messages.append('<Дата рождения> не соответствует формату ДД.ММ.ГГГГ ={}'.format(self.birthday))
        else:
            self.critical_messages.append('обязательное поле <Дата рождения> не содержит значения')
        # проверка повторной идентификации СНИЛС
        if self.picked_snils.is_already_exists and self.picked_snils.value:
            persons = []
            models = self._session_.query(LinkedPerson).filter(LinkedPerson.picked_snils_id == self.picked_snils.id).all()
            for model in models:
                if model.id != self.id:
                    persons.append('<{} {} {} ({})>'.format(
                        model.picked_last_name.value,
                        model.picked_first_name.value,
                        model.picked_middle_name.value,
                        model.birthday
                    ))
            if persons:
                self.warning_messages.append('<СНИЛС> уже идентифицировался ({})'.format(', '.join(persons)))
        # проверка повторной идентификации персоны
        if self.is_already_exists:
            self.warning_messages.append('<Персона> уже идентифицировалась {}'.format(DTConvert(self.created_utc).dtstring))  # должно быть дата/время
        # сбор всех ошибок
        self.warning_messages = (self.warning_messages + self.picked_snils.warning_messages + self.picked_last_name.warning_messages +
                                 self.picked_first_name.warning_messages + self.picked_middle_name.warning_messages)
        self.critical_messages = (self.critical_messages + self.picked_snils.critical_messages + self.picked_last_name.critical_messages +
                                  self.picked_first_name.critical_messages + self.picked_middle_name.critical_messages)


class LinkedDocumentHandler(BaseHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, LinkedDocument)
        self.picked_serial = PickedDocumentSerialHandler(session, keywords['serial'])
        self.picked_number = PickedDocumentNumberHandler(session, keywords['number'])
        self.picked_organization = PickedDocumentOrganizationHandler(session, keywords['organization'])
        self.eskk_document_type_id = clear_string(keywords['eskk_document_type_id'])
        self.date = clear_string(keywords['date'])
        self.get_model()
        self.check()

    @property
    def document_date(self):
        return DTConvert(self.date).date  # должна быть строка

    def is_document_type_exists(self):
        model = self._session_.query(EskkDocumentType).filter(
            EskkDocumentType.id == self.eskk_document_type_id
        ).scalar()
        if model:
            return True
        else:
            self.critical_messages.append('обязательное поле <Тип документа> содержит недопустимое значение ={}'.format(self.eskk_document_type_id))
            self.eskk_document_type_id = '0'
            return False

    def _find_(self):
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.eskk_document_type_id == self.eskk_document_type_id,
            self._class_name_.picked_serial_id == self.picked_serial.id,
            self._class_name_.picked_number_id == self.picked_number.id
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc
            # сверка организации и даты выдачи
            if model.picked_organization_id != self.picked_organization.id:
                self.warning_messages.append('<Документ> идентифицировался ранее с выдавшим органом {}'.format(model.picked_organization.value))
            if model.date != self.date:
                self.warning_messages.append('<Документ> идентифицировался ранее с датой выдачи {}'.format(model.date))

    def get_model(self):
        self.is_document_type_exists()
        self._find_()
        if not self.is_already_exists:
            self.model = self._class_name_()
            # self.model = LinkedDocument()
            self.model.id = self.id
            self.model.created_utc = self.created_utc

            self.model.picked_serial_id = self.picked_serial.id
            if self.picked_serial.model:
                self.model.picked_serial = self.picked_serial.model

            self.model.picked_number_id = self.picked_number.id
            if self.picked_number.model:
                self.model.picked_number = self.picked_number.model

            self.model.picked_organization_id = self.picked_organization.id
            if self.picked_organization.model:
                self.model.picked_organization = self.picked_organization.model

            self.model.eskk_document_type_id = self.eskk_document_type_id
            self.model.date = self.date

            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        # проверка даты документа
        if self.date:
            if self.document_date:
                if self.document_date > DTConvert().date:
                    self.critical_messages.append('<Дата документа> содержит значение старше текущей даты ={}'.format(self.date))
            else:
                self.critical_messages.append('<Дата документа> не соответствует формату ДД.ММ.ГГГГ ={}'.format(self.date))
        else:
            self.critical_messages.append('обязательное поле <Дата документа> не содержит значения')
        # проверка данных паспорта
        if self.eskk_document_type_id == '21':
            if not re_full_match('\d{4}', self.picked_serial.value):
                self.critical_messages.append('<Серия> для типа документа <Паспорт> не соответствует формату ={}'.format(self.picked_serial.value))
            if not re_full_match('\d{6}', self.picked_number.value):
                self.critical_messages.append('<Номер> для типа документа <Паспорт> не соответствует формату ={}'.format(self.picked_number.value))
        # сбор всех ошибок
        self.warning_messages = (self.warning_messages + self.picked_serial.warning_messages + self.picked_number.warning_messages +
                                 self.picked_organization.warning_messages)
        self.critical_messages = (self.critical_messages + self.picked_serial.critical_messages + self.picked_number.critical_messages +
                                  self.picked_organization.critical_messages)


class LinkedDocumentVBDHandler(BaseHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, LinkedDocumentVBD)
        self.picked_serial = PickedDocumentSerialHandler(session, keywords['serial'])
        self.picked_number = PickedDocumentNumberHandler(session, keywords['number'])
        self.picked_organization = PickedDocumentOrganizationHandler(session, keywords['organization'])
        self.date = clear_string(keywords['date'])
        self.get_model()
        self.check()

    @property
    def document_date(self):
        return DTConvert(self.date).date  # должна быть строка

    def _find_(self):
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.picked_serial_id == self.picked_serial.id,
            self._class_name_.picked_number_id == self.picked_number.id
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc
            # сверка организации и даты выдачи
            if model.picked_organization_id != self.picked_organization.id:
                self.warning_messages.append('<УВБД> идентифицировалось ранее с выдавшим органом {}'.format(model.picked_organization.value))
            if model.date != self.date:
                self.warning_messages.append('<УВБД> идентифицировалось ранее с датой выдачи {}'.format(model.date))

    def get_model(self):
        self._find_()
        if not self.is_already_exists:
            # self.model = self._class_name_()
            self.model = LinkedDocumentVBD()
            self.model.id = self.id
            self.model.created_utc = self.created_utc

            self.model.picked_serial_id = self.picked_serial.id
            if self.picked_serial.model:
                self.model.picked_serial = self.picked_serial.model

            self.model.picked_number_id = self.picked_number.id
            if self.picked_number.model:
                self.model.picked_number = self.picked_number.model

            self.model.picked_organization_id = self.picked_organization.id
            if self.picked_organization.model:
                self.model.picked_organization = self.picked_organization.model

            self.model.date = self.date

            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        # проверка даты документа
        if self.date:
            if self.document_date:
                if self.document_date > DTConvert().date:
                    self.critical_messages.append('<Дата УВБД> содержит значение старше текущей даты ={}'.format(self.date))
                elif self.document_date < DTConvert('01.01.2004').date:  # должна быть строка
                    self.critical_messages.append('<Дата УВБД> содержит значение младше 01.01.2004 ={}'.format(self.date))
            else:
                self.critical_messages.append('<Дата УВБД> не соответствует формату ДД.ММ.ГГГГ ={}'.format(self.date))
        else:
            self.critical_messages.append('обязательное поле <Дата УВБД> не содержит значения')
        # проверка серии
        if not re_full_match('[А-Я]{2}', self.picked_serial.value):
            self.critical_messages.append('<Серия УВБД> не соответствует формату ={}'.format(self.picked_serial.value))
        # проверка номера
        if not re_full_match('\d{6,7}', self.picked_number.value):
            self.critical_messages.append('<Номер УВБД> не соответствует формату ={}'.format(self.picked_number.value))
        # проверка номеров по серии
        if self.picked_serial.value in ['ВВ', 'БД']:
            if not re_full_match('\d{6}', self.picked_number.value):
                self.critical_messages.append('<Номер УВБД> для серии {} не соответствует формату ={}'.format(self.picked_serial.value, self.picked_number.value))
        # сбор всех ошибок
        self.warning_messages = (self.warning_messages + self.picked_serial.warning_messages +
                                 self.picked_number.warning_messages + self.picked_organization.warning_messages)
        self.critical_messages = (self.critical_messages + self.picked_serial.critical_messages +
                                  self.picked_number.critical_messages + self.picked_organization.critical_messages)


class LinkedAddressHandler(BaseHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, LinkedAddress)
        self.picked_index = PickedAddressIndexHandler(session, keywords['index'])
        self.picked_region = PickedAddressRegionHandler(session, keywords['region'])
        self.picked_area = PickedAddressAreaHandler(session, keywords['area'])
        self.picked_locality = PickedAddressLocalityHandler(session, keywords['locality'])
        self.picked_street = PickedAddressStreetHandler(session, keywords['street'])
        self.picked_house = PickedAddressHouseHandler(session, keywords['house'])
        self.picked_building = PickedAddressBuildingHandler(session, keywords['building'])
        self.picked_flat = PickedAddressFlatHandler(session, keywords['flat'])
        self.get_model()
        self.check()

    def _find_(self):
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.picked_index_id == self.picked_index.id,
            self._class_name_.picked_region_id == self.picked_region.id,
            self._class_name_.picked_area_id == self.picked_area.id,
            self._class_name_.picked_locality_id == self.picked_locality.id,
            self._class_name_.picked_street_id == self.picked_street.id,
            self._class_name_.picked_house_id == self.picked_house.id,
            self._class_name_.picked_building_id == self.picked_building.id,
            self._class_name_.picked_flat_id == self.picked_flat.id
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc

    def get_model(self):
        self._find_()
        if not self.is_already_exists:
            # self.model = self._class_name_()
            self.model = LinkedAddress()
            self.model.id = self.id
            self.model.created_utc = self.created_utc

            self.model.picked_index_id = self.picked_index.id
            if self.picked_index.model:
                self.model.picked_index = self.picked_index.model

            self.model.picked_region_id = self.picked_region.id
            if self.picked_region.model:
                self.model.picked_region = self.picked_region.model

            self.model.picked_area_id = self.picked_area.id
            if self.picked_area.model:
                self.model.area = self.picked_area.model

            self.model.picked_locality_id = self.picked_locality.id
            if self.picked_locality.model:
                self.model.picked_locality = self.picked_locality.model

            self.model.picked_street_id = self.picked_street.id
            if self.picked_street.model:
                self.model.picked_street = self.picked_street.model

            self.model.picked_house_id = self.picked_house.id
            if self.picked_house.model:
                self.model.picked_house = self.picked_house.model

            self.model.picked_building_id = self.picked_building.id
            if self.picked_building.model:
                self.model.picked_building = self.picked_building.model

            self.model.picked_flat_id = self.picked_flat.id
            if self.picked_flat.model:
                self.model.picked_flat = self.picked_flat.model

            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        self.warning_messages = (self.warning_messages + self.picked_index.warning_messages +
                                 self.picked_region.warning_messages + self.picked_area.warning_messages +
                                 self.picked_locality.warning_messages + self.picked_street.warning_messages +
                                 self.picked_house.warning_messages + self.picked_building.warning_messages +
                                 self.picked_flat.warning_messages)
        self.critical_messages = (self.critical_messages + self.picked_index.critical_messages +
                                  self.picked_region.critical_messages + self.picked_area.critical_messages +
                                  self.picked_locality.critical_messages + self.picked_street.critical_messages +
                                  self.picked_house.critical_messages + self.picked_building.critical_messages +
                                  self.picked_flat.critical_messages)


class LinkedOrderFIOHandler(BaseHandler):

    def __init__(self, session, value):
        super().__init__(session, LinkedOrderFIO)
        fio_list = get_fio_list(value)
        self.picked_last_name = PickedLastNameHandler(session, fio_list[0])
        self.picked_first_name = PickedFirstNameHandler(session, fio_list[1])
        self.picked_middle_name = PickedMiddleNameHandler(session, fio_list[2])
        self.get_model()
        self.check()

    def _find_(self):
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.picked_last_name_id == self.picked_last_name.id,
            self._class_name_.picked_first_name_id == self.picked_first_name.id,
            self._class_name_.picked_middle_name_id == self.picked_middle_name.id,
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc

    def get_model(self):
        self._find_()
        if not self.is_already_exists:
            # self.model = self._class_name_()
            self.model = LinkedOrderFIO()
            self.model.id = self.id
            self.model.created_utc = self.created_utc

            self.model.picked_last_name_id = self.picked_last_name.id
            if self.picked_last_name.model:
                self.model.picked_last_name = self.picked_last_name.model

            self.model.picked_first_name_id = self.picked_first_name.id
            if self.picked_first_name.model:
                self.model.picked_first_name = self.picked_first_name.model

            self.model.picked_middle_name_id = self.picked_middle_name.id
            if self.picked_middle_name.model:
                self.model.picked_middle_name = self.picked_middle_name.model

            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        # сбор всех ошибок
        self.warning_messages = (self.warning_messages + self.picked_last_name.warning_messages +
                                 self.picked_first_name.warning_messages + self.picked_middle_name.warning_messages)
        self.critical_messages = (self.critical_messages + self.picked_last_name.critical_messages +
                                  self.picked_first_name.critical_messages + self.picked_middle_name.critical_messages)


class LinkedOrderPersonHandler(BaseHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, LinkedOrderPerson)
        self.picked_military_rank = PickedMilitaryRankHandler(session, keywords['rank'])
        self.picked_personal_number = PickedPersonalNumberHandler(session, keywords['personal_number'])
        self.picked_military_subject = PickedMilitarySubjectHandler(session, keywords['subject'])
        self.linked_order_fio = LinkedOrderFIOHandler(session, keywords['fio'])
        self.get_model()
        self.check()

    @property
    def person_appeal(self):
        return '{} {} {} {} ({})'.format(
            self.picked_military_rank.value,
            self.linked_order_fio.picked_last_name.value,
            self.linked_order_fio.picked_first_name.value,
            self.linked_order_fio.picked_middle_name.value,
            self.picked_personal_number.value
        )

    def _find_(self):
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.picked_military_rank_id == self.picked_military_rank.id,
            self._class_name_.picked_personal_number_id == self.picked_personal_number.id,
            self._class_name_.picked_military_subject_id == self.picked_military_subject.id,
            self._class_name_.linked_order_fio_id == self.linked_order_fio.id
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc

    def get_model(self):
        self._find_()
        if not self.is_already_exists:
            # self.model = self._class_name_()
            self.model = LinkedOrderPerson()
            self.model.id = self.id
            self.model.created_utc = self.created_utc

            self.model.picked_military_rank_id = self.picked_military_rank.id
            if self.picked_military_rank.model:
                self.model.picked_military_rank = self.picked_military_rank.model

            self.model.picked_personal_number_id = self.picked_personal_number.id
            if self.picked_personal_number.model:
                self.model.picked_personal_number = self.picked_personal_number.model

            self.model.picked_military_subject_id = self.picked_military_subject.id
            if self.picked_military_subject.model:
                self.model.picked_military_subject = self.picked_military_subject.model

            self.model.linked_order_fio_id = self.linked_order_fio.id
            if self.linked_order_fio.model:
                self.model.linked_order_fio = self.linked_order_fio.model

            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        if self.is_already_exists:
            self.warning_messages.append('<Персона> уже идентифицировалась в приказах')

        self.warning_messages = (self.warning_messages + self.picked_military_rank.warning_messages +
                                 self.picked_personal_number.warning_messages + self.picked_military_subject.warning_messages +
                                 self.linked_order_fio.warning_messages)

        self.critical_messages = (self.critical_messages + self.picked_military_rank.critical_messages +
                                  self.picked_personal_number.critical_messages + self.picked_military_subject.critical_messages +
                                  self.linked_order_fio.critical_messages)


class LinkedDefenderHandler(BaseHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, LinkedDefender)
        self.linked_person = LinkedPersonHandler(session, **keywords['person'])
        self.linked_document = LinkedDocumentHandler(session, **keywords['document'])
        self.linked_document_vbd = LinkedDocumentVBDHandler(session, **keywords['document_vbd'])
        self.linked_reg_address = LinkedAddressHandler(session, **keywords['reg_address'])
        self.linked_fact_address = LinkedAddressHandler(session, **keywords['fact_address'])
        self.picked_military_subject = PickedMilitarySubjectHandler(session, keywords['subject_name'])
        self.picked_personal_number = PickedPersonalNumberHandler(session, keywords['personal_number'])
        self.birth_place = clear_string(keywords['birth_place'])
        self.exclude_date = clear_string(keywords['exclude_date'])
        self.exclude_order = clear_string(keywords['exclude_order'])
        self.id_ern = clear_string(keywords['id_ern'])
        self.get_model()
        self.check()

    @property
    def exclude_real_date(self):
        return DTConvert(self.exclude_date).date  # должна быть строка

    @property
    def is_success(self):
        return False if self.critical_messages else True

    @property
    def status(self):
        if self.critical_messages:
            return 'Критические ошибки, валидация не пройдена'
        elif self.warning_messages:
            return 'Валидация пройдена с предупреждениями'
        else:
            return 'Валидация пройдена успешно'

    def _find_(self):
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.linked_person_id == self.linked_person.id,
            self._class_name_.linked_document_id == self.linked_document.id,
            self._class_name_.linked_document_vbd_id == self.linked_document_vbd.id,
            self._class_name_.linked_reg_address_id == self.linked_reg_address.id,
            self._class_name_.linked_fact_address_id == self.linked_fact_address.id,
            self._class_name_.picked_military_subject_id == self.picked_military_subject.id,
            self._class_name_.picked_personal_number_id == self.picked_personal_number.id,
            self._class_name_.birth_place == self.birth_place,
            self._class_name_.exclude_date == self.exclude_date,
            self._class_name_.exclude_order == self.exclude_order,
            self._class_name_.id_ern == self.id_ern
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc

    def get_model(self):
        self._find_()
        if not self.is_already_exists:
            self.model = LinkedDefender()
            self.model.id = self.id
            self.model.created_utc = self.created_utc

            self.model.linked_person_id = self.linked_person.id
            if self.linked_person.model:
                self.model.linked_person = self.linked_person.model

            self.model.linked_document_id = self.linked_document.id
            if self.linked_document.model:
                self.model.linked_document = self.linked_document.model

            self.model.linked_document_vbd_id = self.linked_document_vbd.id
            if self.linked_document_vbd.model:
                self.model.linked_document_vbd = self.linked_document_vbd.model

            self.model.linked_reg_address_id = self.linked_reg_address.id
            if self.linked_reg_address.model:
                self.model.linked_reg_address = self.linked_reg_address.model

            self.model.linked_fact_address_id = self.linked_fact_address.id
            if self.linked_fact_address.model:
                self.model.linked_fact_address = self.linked_fact_address.model

            self.model.picked_military_subject_id = self.picked_military_subject.id
            if self.picked_military_subject.model:
                self.model.picked_military_subject = self.picked_military_subject.model

            self.model.picked_personal_number_id = self.picked_personal_number.id
            if self.picked_personal_number.model:
                self.model.picked_personal_number = self.picked_personal_number.model

            self.model.birth_place = self.birth_place
            self.model.exclude_date = self.exclude_date
            self.model.exclude_order = self.exclude_order
            self.model.id_ern = self.id_ern

            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        # проверка на идентификацию защитника с такими же данными
        if self.is_already_exists:
            self.warning_messages.append('<Защитник> уже идентифицировался {}'.format(self.created_utc))
        # проверка принадлежности существующего документа этой же персоне
        if self.linked_document.is_already_exists and self.linked_document.picked_serial.value and self.linked_document.picked_number.value:
            models = self._session_.query(LinkedDefender).filter(LinkedDefender.linked_document_id == self.linked_document.id).all()
            for model in models:
                if model.linked_person_id != self.linked_person.id:
                    self.warning_messages.append('<Документ> {} № {} идентифицировался ранее у персоны {} {} {}'.format(
                        model.linked_document.picked_serial.value,
                        model.linked_document.picked_number.value,
                        model.linked_person.picked_last_name.value,
                        model.linked_person.picked_first_name.value,
                        model.linked_person.picked_middle_name.value
                    ))
        # проверка принадлежности существующего УВБД этой же персоне
        if self.linked_document_vbd.is_already_exists and self.linked_document_vbd.picked_serial.value and self.linked_document_vbd.picked_number.value:
            models = self._session_.query(LinkedDefender).filter(LinkedDefender.linked_document_vbd_id == self.linked_document_vbd.id).all()
            for model in models:
                if model.linked_person_id != self.linked_person.id:
                    self.warning_messages.append('<УВБД> {} № {} идентифицировалось ранее у персоны {} {} {}'.format(
                        model.linked_document.picked_serial.value,
                        model.linked_document.picked_number.value,
                        model.linked_person.picked_last_name.value,
                        model.linked_person.picked_first_name.value,
                        model.linked_person.picked_middle_name.value
                    ))
        # проверка принадлежности существующего личного номера этой же персоне
        if self.picked_personal_number.is_already_exists and self.picked_personal_number.value:
            models = self._session_.query(LinkedDefender).filter(LinkedDefender.picked_personal_number_id == self.picked_personal_number.id).all()
            for model in models:
                if model.linked_person_id != self.linked_person.id:
                    self.warning_messages.append('<Личный номер> {} идентифицировался ранее у персоны {} {} {}'.format(
                        model.picked_personal_number.value,
                        model.linked_person.picked_last_name.value,
                        model.linked_person.picked_first_name.value,
                        model.linked_person.picked_middle_name.value
                    ))
        # проверка даты исключения
        if self.exclude_date:
            if self.exclude_real_date:
                if self.exclude_real_date > DTConvert().date:
                    self.critical_messages.append('<Дата исключения> старше текущей даты ={}'.format(self.exclude_date))
            else:
                self.critical_messages.append('<Дата исключения> не соответствует формату ДД.ММ.ГГГГ ={}'.format(self.exclude_date))
        else:
            self.critical_messages.append('обязательное поле <Дата исключения> не содержит значения')
        # проверка реквизитов приказа об исключении
        if self.exclude_order:
            if len(self.exclude_order) < 13:
                self.warning_messages.append('<Реквизиты приказа> содержат излишне короткое значение')
        else:
            self.critical_messages.append('обязательное поле <Реквизиты приказа> не содержит значения')
        # проверка места рождения
        if self.birth_place:
            if not re_full_match('[А-Яа-я0-9-,.()\/ ]+', self.birth_place):
                self.critical_messages.append('<Место рождения> не соответствует формату ={}'.format(self.birth_place))
            if len(self.birth_place) < 5 or len(self.birth_place) > 200:
                self.critical_messages.append('<Место рождения> недопустимая длина значения {}={} (должно быть 5-200)'.format(
                    self.birth_place, len(self.birth_place)
                ))
        # проверка идентификатора единого реестра населения
        if self.id_ern:
            if not re_full_match('\d{12}', self.id_ern):
                self.critical_messages.append('<ID ЕРН> не соответствует формату ={}'.format(self.id_ern))
        # проверка действительности паспорта
        if self.linked_document.eskk_document_type_id == '21':
            if self.linked_document.document_date and self.linked_person.age(20) and self.linked_document.document_date < self.linked_person.age(20) < DTConvert().date:
                self.warning_messages.append('<Паспорт> требует замены по достижению возраста 20 лет')
            if self.linked_document.document_date and self.linked_person.age(45) and self.linked_document.document_date < self.linked_person.age(45) < DTConvert().date:
                self.warning_messages.append('<Паспорт> требует замены по достижению возраста 45 лет')
        # проверка даты выдачи УВБД
        if self.linked_person.age(18) and self.linked_document_vbd.document_date and self.linked_person.age(18) > self.linked_document_vbd.document_date:
            self.critical_messages.append('<УВБД> получено до достижения возраста 18 лет')
        # сбор всех ошибок
        self.warning_messages = (self.warning_messages + self.linked_person.warning_messages +
                                 self.linked_document.warning_messages + self.linked_document_vbd.warning_messages +
                                 self.linked_reg_address.warning_messages + self.linked_fact_address.warning_messages +
                                 self.picked_military_subject.warning_messages + self.picked_personal_number.warning_messages)
        self.critical_messages = (self.critical_messages + self.linked_person.critical_messages +
                                  self.linked_document.critical_messages + self.linked_document_vbd.critical_messages +
                                  self.linked_reg_address.critical_messages + self.linked_fact_address.critical_messages +
                                  self.picked_military_subject.critical_messages + self.picked_personal_number.critical_messages)


class LinkedOrderPersonPeriodHandler(BaseHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, LinkedOrderPersonPeriod)
        self.linked_order_person = LinkedOrderPersonHandler(session, **keywords)
        # периоды преобразуем в списки
        # print(keywords['date_begin'], keywords['date_end'])
        self.begin_list = clear_string(keywords['date_begin']).replace(' 00:00:00', '').split(' ')  # должна быть дата
        self.end_list = clear_string(keywords['date_end']).replace(' 00:00:00', '').split(' ')  # должна быть дата

        # self.begin_list = clear_string(DTConvert(keywords['date_begin']).dstring).split(' ')  # должна быть дата
        # self.end_list = clear_string(DTConvert(keywords['date_end']).dstring).split(' ')  # должна быть дата
        # оставляем пустыми для парсинга
        self.date_begin = None
        self.date_end = None
        self.get_model()

    @property
    def date_begin_real(self):
        return DTConvert(self.date_begin).date  # должна быть строка

    @property
    def date_end_real(self):
        return DTConvert(self.date_end).date  # должна быть строка

    @property
    def days_count(self):
        start = self.date_begin_real
        stop = self.date_end_real
        if start and stop:
            return (stop - start).days + 1
        else:
            return 0

    def _find_(self):
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.linked_order_person_id == self.linked_order_person.id,
            self._class_name_.date_begin == self.date_begin,
            self._class_name_.date_end == self.date_end
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc

    def get_model(self):
        # TODO парсить периоды по частям и запускать обработку
        if len(self.begin_list) != len(self.end_list):
            self.critical_messages.append('ошибка количества периодов {} [{}], [{}]'.format(
                self.linked_order_person.person_appeal,
                self.begin_list,
                self.end_list
            ))
        else:
            # print(self.begin_list)
            # print(self.end_list)
            # input('->')
            for index in range(0, len(self.begin_list)):
                self.date_begin = self.begin_list[index]
                self.date_end = self.end_list[index]

                self._find_()
                self.check()
                if not self.is_already_exists:
                    # self.model = self._class_name_()
                    self.model = LinkedOrderPersonPeriod()
                    self.model.id = str(uuid4())
                    self.model.created_utc = DTConvert().datetime
                    self.model.linked_order_person_id = self.linked_order_person.id
                    self.model.date_begin = self.date_begin
                    self.model.date_end = self.date_end
                    self.model.days_count = self.days_count

                    self._session_.add(self.model)
                    self._session_.flush()

    def check(self):
        if self.is_already_exists:
            self.warning_messages.append('<Период> {}-{} для персоны {} уже добавлялся'.format(
                DTConvert(self.date_begin).dstring, DTConvert(self.date_end).dstring, self.linked_order_person.person_appeal
            ))
        if not self.date_begin_real:
            self.critical_messages.append('<Начало периода> не соответствует формату ={}'.format(self.date_begin))
        if not self.date_end_real:
            self.critical_messages.append('<Окончание периода> не соответствует формату ={}'.format(self.date_end))
        if self.days_count <= 0:
            self.critical_messages.append('невозможно рассчитать количество дней в периоде {}-{}'.format(self.date_begin, self.date_end))
