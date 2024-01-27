from abc import abstractmethod
from sqlalchemy.sql.operators import ilike_op

from database import KeepedReport, EskkMilitarySubject, KeepedReportRecord, LinkedOrderFIO, LinkedOrderPerson, \
    PickedPersonalNumber, KeepedOrder, KeepedOrderRecord, LinkedOrderPersonPeriod
from modules.loader.order import OrdersWorkbookPXL
from tools.fs import File, Directory
from tools.date_and_time import date_to_string
# from tools import base_filename, filename_extension, get_new_path, copy_file, application_relpath
from . import BaseHandler
from modules.loader.defender import DefendersWorkbook
from .linker import LinkedDefenderHandler, LinkedOrderPersonPeriodHandler


class KeeperRecordHandler(BaseHandler):

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


class KeepedReportRecordHandler(KeeperRecordHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, KeepedReportRecord, **keywords['record'])
        self.linked_defender = LinkedDefenderHandler(session, **keywords['defender'])
        self.keeped_report_id = keywords['keeped_report_id']
        self.is_find_in_orders = False
        self.check()
        self.get_model()

    def _find_by_fio_(self):
        model = self._session_.query(LinkedOrderFIO).filter(
            LinkedOrderFIO.picked_last_name_id == self.linked_defender.linked_person.picked_last_name.id,
            LinkedOrderFIO.picked_first_name_id == self.linked_defender.linked_person.picked_first_name.id,
            LinkedOrderFIO.picked_middle_name_id == self.linked_defender.linked_person.picked_middle_name.id
        ).scalar()
        if not model:
            self.warning_messages.append('<ФИО> отсутствует в приказах')
        return model

    def _find_by_personal_number(self):
        models = self._session_.query(LinkedOrderPerson).join(PickedPersonalNumber).filter(
            ilike_op(PickedPersonalNumber.value, '%{}%'.format(self.linked_defender.picked_personal_number.value))
        ).all()
        if not models:
            self.warning_messages.append('<Личный номер> отсутствует в приказах ={}'.format(
                self.linked_defender.picked_personal_number.value
            ))
        return models

    def _find_(self):
        fio_model = self._find_by_fio_()
        person_models = self._find_by_personal_number()
        if fio_model:
            if person_models:
                for person in person_models:
                    if person.linked_order_fio_id == fio_model.id:
                        self.is_find_in_orders = True
        if not self.is_find_in_orders:
            self.critical_messages.append('<Персона> отсутствует в приказах')

    def get_model(self):
        self._find_()
        self.model = KeepedReportRecord()
        self.model.id = self.id
        self.model.created_utc = self.created_utc
        self.model.keeped_report_id = self.keeped_report_id
        self.model.keep_row_num = self.keep_row_num
        self.model.file_row_num = self.file_row_num
        self.model.linked_defender_id = self.linked_defender.id
        if self.linked_defender.model:
            self.model.linked_defender = self.linked_defender.model
        self.model.is_find_in_orders = self.is_find_in_orders
        self.model.warning_messages = self.warning
        self.model.critical_messages = self.critical

        self._session_.add(self.model)
        self._session_.flush()

    def check(self):
        self.warning_messages += self.linked_defender.warning_messages
        self.critical_messages += self.linked_defender.critical_messages


class KeepedOrderRecordHandler(KeeperRecordHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, KeepedOrderRecord, **keywords['record'])

        self.linked_order_person_period = LinkedOrderPersonPeriodHandler(session, **keywords['person_period'])
        self.keeped_order_id = keywords['keeped_order_id']
        self.check()
        self.get_model()

    def _find_(self):
        # не используется
        pass

    def get_model(self):
        self.model = KeepedOrderRecord()
        self.model.id = self.id
        self.model.created_utc = self.created_utc
        self.model.keeped_order_id = self.keeped_order_id
        self.model.keep_row_num = self.keep_row_num
        self.model.file_row_num = self.file_row_num
        self.model.linked_order_person_period_id = self.linked_order_person_period.id
        if self.linked_order_person_period.model:
            self.model.linked_order_person_period = self.linked_order_person_period.model
        self.model.warning_messages = self.warning
        self.model.critical_messages = self.critical

        self._session_.add(self.model)
        self._session_.flush()

    def check(self):
        self.warning_messages = self.linked_order_person_period.warning_messages
        self.critical_messages = self.linked_order_person_period.critical_messages


class KeeperFileHandler(BaseHandler):

    def __init__(self, session, class_model):
        super().__init__(session, class_model)
        self.workbook = None
        self.original_file_path = None
        self.file_path = None
        self.file_relpath = None

    @abstractmethod
    def _find_(self):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def check(self):
        pass


class KeepedReportHandler(KeeperFileHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, KeepedReport)
        self.eskk_military_subject_id = keywords['workbook']['subject_id']
        self.contact_info = keywords['contact_info']
        # номер импорта и хэш-сумма файла
        self.workbook = DefendersWorkbook(**keywords['workbook'])
        # ищем загруженный файл с такой хэш-суммой
        self._find_()
        # путь к файлу выбранному оператором
        # self.original_file_path = File(keywords['workbook']['file_path'])
        # путь к копии файла в хранилище

        self.destination = Directory(keywords['workbook']['destination'])
        self.file = File(
            self.destination.add_file(
                self.workbook.import_id + self.workbook.file.extension
            )
        )

        # self.file_path = get_new_path(
        #     keywords['workbook']['destination'],
        #     self.workbook.import_id + self.workbook.file.extension
        # )
        # относительный путь к копии файла в хранилище
        # self.file_relpath = application_relpath(self.file_path)
        # копирование файла
        if not self.is_model_exists:
            self.workbook.file.copy(self.file.path)
            # copy_file(self.original_file_path, self.file_path)
            # чтение содержимого книги
            self.workbook.load_workbook(self.file.path)
        # получение модели импорта
        self.get_model()

    def transform_row(self, row_ind, row_val):
        """Преобразование строки данных в словарь"""
        result = {
            'record': {
                'keep_row_num': row_ind + 1,
                'file_row_num': row_ind + 3
            },
            'defender': {
                'person': {
                    'last_name': row_val[0],
                    'first_name': row_val[1],
                    'middle_name': row_val[2],
                    'eskk_gender_id': row_val[3],
                    'birthday': date_to_string(row_val[4]),
                    'snils': row_val[6]
                },
                'birth_place': row_val[5],
                'document': {
                    'eskk_document_type_id': row_val[7],
                    'serial': row_val[8],
                    'number': row_val[9],
                    'date': date_to_string(row_val[10]),
                    'organization': row_val[11]
                },
                'document_vbd': {
                    'serial': row_val[12],
                    'number': row_val[13],
                    'date': date_to_string(row_val[14]),
                    'organization': row_val[15]
                },
                'reg_address': {
                    'index': row_val[16],
                    'region': row_val[17],
                    'area': row_val[18],
                    'locality': row_val[19],
                    'street': row_val[20],
                    'house': row_val[21],
                    'building': row_val[22],
                    'flat': row_val[23]
                },
                'fact_address': {
                    'index': row_val[24],
                    'region': row_val[25],
                    'area': row_val[26],
                    'locality': row_val[27],
                    'street': row_val[28],
                    'house': row_val[29],
                    'building': row_val[30],
                    'flat': row_val[31]
                },
                'id_ern': row_val[32],
                'subject_name': row_val[33],
                'exclude_date': date_to_string(row_val[34]),
                'exclude_order': row_val[35],
                'personal_number': row_val[36]
            },
            'keeped_report_id': self.workbook.import_id
        }
        return result

    def parsing(self):
        """Парсин данных"""
        self._session_.add(self.model)
        self._session_.flush()

        for row_ind, row_val in enumerate(self.workbook.get_defenders_worksheet_data()[2:]):
            if row_val[0]:
                KeepedReportRecordHandler(self._session_, **self.transform_row(row_ind, row_val))
            else:
                break
        self.model.is_loaded = True
        self._session_.flush()

    def is_subject_exists(self):
        """Проверка существования субъекта в ЕСКК"""
        model = self._session_.query(EskkMilitarySubject).filter(
            EskkMilitarySubject.id == self.eskk_military_subject_id
        ).scalar()
        return True if model else False

    def _find_(self):
        """Поиск импорта по хэш-сумме файла"""
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.hash_sum == self.workbook.file.md5()
        ).scalar()
        if model:
            self.is_model_exists = True
            self.id = model.id
            self.created_utc = model.created_utc
            self.eskk_military_subject_id = model.eskk_military_subject_id
            self.contact_info = model.contact_info

    def get_model(self):
        self.check()
        if not self.is_model_exists and self.workbook.file.md5():
            self.model = KeepedReport()
            self.model.id = self.workbook.import_id
            self.model.created_utc = self.created_utc
            self.model.hash_sum = self.workbook.file.md5()
            self.model.original_filename = self.original_file_path  # хуй знает
            self.model.instance_filename = self.file_relpath
            self.model.is_on_template = self.workbook.is_correct
            self.model.eskk_military_subject_id = self.eskk_military_subject_id
            self.model.contact_info = self.contact_info
            self.model.note = self.critical

    def check(self):
        if self.is_model_exists:
            self.critical_messages.append('<Файл> уже загружался, хэш-сумма {}, номер импорта {}'.format(
                self.workbook.hashsum, self.id
            ))
        else:
            if not self.is_subject_exists():
                self.critical_messages.append('неизвестный <Субъект> с идентификатором {}'.format(self.eskk_military_subject_id))
            if not self.workbook.is_correct:
                self.critical_messages.append('<Файл> некорректный {}'.format(self.workbook.log))


class KeepedOrderHandler(KeeperFileHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, KeepedOrder)
        # номер импорта и хэш-сумма файла
        # self.workbook = OrdersWorkbook(**keywords)
        self.workbook = OrdersWorkbookPXL(keywords['file_path'])
        # ищем загруженный файл с такой хэш-суммой
        self._find_()
        # путь к файлу выбранному оператором
        self.original_file_path = self.workbook.filepath
        # путь к копии файла в хранилище
        self.file_path = get_new_path(
            keywords['destination'],
            self.workbook.import_id + filename_extension(self.workbook.filename))
        # относительный путь к копии файла в хранилище
        self.file_relpath = application_relpath(self.file_path)
        # копирование файла
        if not self.is_already_exists:
            copy_file(self.original_file_path, self.file_path)
            # чтение содержимого книги
            # self.workbook.load_workbook(self.file_path)
            self.workbook.load_workbook()
        # получение модели импорта
        self.get_model()

    def transform_row(self, row_ind, row_val):
        """Преобразование строки данных в словарь"""
        result = {
            'record': {
                'keep_row_num': row_ind + 1,
                'file_row_num': row_ind + 4
            },
            'person_period': {
                'fio': row_val[0].value,
                'rank': row_val[1].value,
                'personal_number': row_val[2].value,
                'subject': row_val[3].value,
                'date_begin': row_val[4].value,
                'date_end': row_val[5].value
            },
            'keeped_order_id': self.workbook.import_id
        }
        return result

    def clear_orders(self):
        print('Очистка содержания приказов...')
        self._session_.query(KeepedOrderRecord).delete()
        self._session_.query(LinkedOrderPersonPeriod).delete()
        self._session_.query(LinkedOrderPerson).delete()
        self._session_.query(LinkedOrderFIO).delete()
        # self._session_.commit()

    def parsing(self):
        """Парсин данных"""
        print('Загрузка приказов...')
        self._session_.add(self.model)
        self._session_.flush()

        print('Обработка СПИСОК')
        for row_ind, row_val in enumerate(self.workbook.main_sheet_rows):
            if row_ind > 2:
                if row_val[0].value:
                    KeepedOrderRecordHandler(self._session_, **self.transform_row(row_ind, row_val))
                    if row_ind % 10000 == 0:
                        print('Обработано', row_ind + 1)
                else:
                    break

        print('Обработка МОБ')
        for row_ind, row_val in enumerate(self.workbook.mob_sheet_rows):
            if row_ind > 2:
                if row_val[0].value:
                    KeepedOrderRecordHandler(self._session_, **self.transform_row(row_ind, row_val))
                    if row_ind % 10000 == 0:
                        print('Обработано', row_ind + 1)
                else:
                    break

        print('Обработка ТЕРР')
        for row_ind, row_val in enumerate(self.workbook.terra_sheet_rows):
            if row_ind > 2:
                if row_val[0].value:
                    KeepedOrderRecordHandler(self._session_, **self.transform_row(row_ind, row_val))
                    if row_ind % 10000 == 0:
                        print('Обработано', row_ind + 1)
                else:
                    break

        self.model.is_loaded = True
        self._session_.flush()

    def _find_(self):
        """Поиск импорта по хэш-сумме файла"""
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.hash_sum == self.workbook.hashsum
        ).scalar()
        if model:
            self.is_already_exists = True
            self.id = model.id
            self.created_utc = model.created_utc

    def get_model(self):
        self.check()
        if not self.is_already_exists and self.workbook.hashsum:
            self.model = KeepedOrder()
            self.model.id = self.workbook.import_id
            self.model.created_utc = self.created_utc
            self.model.hash_sum = self.workbook.hashsum
            self.model.original_filename = self.original_file_path
            self.model.instance_filename = self.file_relpath
            self.model.is_on_template = True if self.workbook.workbook else False
            self.model.note = self.critical

    def check(self):
        if self.is_already_exists:
            self.critical_messages.append('<Файл> уже загружался, хэш-сумма {}, номер импорта {}'.format(
                self.workbook.hashsum, self.id
            ))
        elif not self.workbook.workbook:
            # self.critical_messages.append('<Файл> некорректный {}'.format(self.workbook.log))
            print('SHIT')
