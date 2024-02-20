from sqlalchemy.sql.operators import ilike_op

from database import EskkMilitarySubject, KeepedOrderRecord, LinkedOrderPersonPeriod
from database import PickedPersonalNumber, KeepedReportRecord, KeepedReport
from database import LinkedOrderFIO, LinkedOrderPerson, KeepedOrder
from tools import DTConvert

from .base import BaseKeeperFileHandler, BaseKeeperRecordHandler
from .linker import LinkedDefenderHandler, LinkedOrderPersonPeriodHandler


class KeepedReportHandler(BaseKeeperFileHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, KeepedReport)
        self.import_id = keywords['import_id']
        self.subject = self.get_subject_model(keywords['subject_id'])
        self.original_filename = keywords['original_filename']
        self.instance_filename = keywords['instance_filename']
        self.hash_sum = keywords['hash_sum']
        self.contact_info = keywords['contact_info']
        self.rows_data = keywords['rows_data']
        self.get_model()
        self.parsing_rows()

    def get_subject_model(self, subject_id):
        model = self._session_.query(EskkMilitarySubject).filter(EskkMilitarySubject.id == subject_id).scalar()
        if model:
            return model
        else:
            raise ValueError('отсутствует субъект с идентификатором <{}>'.format(subject_id))

    def _find_(self):
        """Поиск импорта по хэш-сумме файла"""
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.hash_sum == self.hash_sum
        ).scalar()
        if model:
            self.is_already_exists = True
            raise SystemError('файл уже был загружен ранее, номер импорта <{}>'.format(model.id))

    def check(self):
        pass

    def get_model(self):
        self._find_()
        self.model = KeepedReport()
        self.model.id = self.import_id
        self.model.created_utc = self.created_utc
        self.model.hash_sum = self.hash_sum
        self.model.original_filename = self.original_filename
        self.model.instance_filename = self.instance_filename
        self.model.is_on_template = True
        self.model.eskk_military_subject_id = self.subject.id
        self.model.contact_info = self.contact_info
        self.model.note = self.critical
        self._session_.add(self.model)
        self._session_.flush()

    def parsing_rows(self):
        """Парсин данных"""
        for row in self.rows_data:
            KeepedReportRecordHandler(self._session_, self.import_id, **row)
        self.model.is_loaded = True
        self._session_.flush()


class KeepedReportRecordHandler(BaseKeeperRecordHandler):

    def __init__(self, session, import_id, **keywords):
        super().__init__(session, KeepedReportRecord, **keywords['record'])
        self.linked_defender = LinkedDefenderHandler(session, **keywords['defender'])
        self.keeped_report_id = import_id
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


class KeepedOrderHandler(BaseKeeperFileHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, KeepedOrder)
        self.checkpoint_count = 10000
        self.import_id = keywords['import_id']
        self.original_filename = keywords['original_filename']
        self.workbook = keywords['workbook']
        self._find_()
        self.clear_orders()
        self.get_model()
        self.parsing()

    def _find_(self):
        """Поиск импорта по хэш-сумме файла"""
        model = self._session_.query(self._class_name_).filter(self._class_name_.hash_sum == self.workbook.file.md5()).scalar()
        if model:
            self.is_already_exists = True
            raise SystemError('файл уже был загружен ранее, номер импорта <{}>'.format(model.id))

    def clear_orders(self):
        print_log('Очистка содержания приказов...')
        self._session_.query(KeepedOrderRecord).delete()
        self._session_.query(LinkedOrderPersonPeriod).delete()
        self._session_.query(LinkedOrderPerson).delete()
        self._session_.query(LinkedOrderFIO).delete()
        self._session_.flush()

    def check(self):
        pass

    def get_model(self):
        print_log('Загрузка приказов (отсчет по {})...'.format(self.checkpoint_count))
        self.model = KeepedOrder()
        self.model.id = self.import_id
        self.model.created_utc = self.created_utc
        self.model.hash_sum = self.workbook.file.md5()
        self.model.original_filename = self.original_filename
        self.model.instance_filename = self.workbook.file.rel_path
        self.model.is_on_template = True
        self.model.note = self.critical
        self._session_.add(self.model)
        self._session_.flush()

    def parsing(self):
        """Парсин данных"""
        for sheet_name in self.workbook.required_worksheets:
            print_log('Лист <{}>'.format(sheet_name))
            self.workbook.select_worksheet(sheet_name)
            for row_ind, row_val in enumerate(self.workbook.worksheet_data()):
                if row_ind > 2:
                    if row_val[0].value:
                        keywords = {
                            'record': {
                                'keep_row_num': row_ind - 2,
                                'file_row_num': row_ind + 1
                            },
                            'person_period': {
                                'fio': row_val[0].value,
                                'rank': row_val[1].value,
                                'personal_number': row_val[2].value,
                                'subject': row_val[3].value,
                                'date_begin': row_val[4].value,
                                'date_end': row_val[5].value
                            }
                        }
                        KeepedOrderRecordHandler(self._session_, self.import_id, **keywords)
                    else:
                        break
                if (row_ind + 1) % self.checkpoint_count == 0:
                    print_log('обработано {} строк'.format(row_ind + 1))
        self.model.is_loaded = True
        self._session_.flush()


class KeepedOrderRecordHandler(BaseKeeperRecordHandler):

    def __init__(self, session, import_id, **keywords):
        super().__init__(session, KeepedOrderRecord, **keywords['record'])
        self.linked_order_person_period = LinkedOrderPersonPeriodHandler(session, **keywords['person_period'])
        self.keeped_order_id = import_id
        self.check()
        self.get_model()

    def _find_(self):
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


def print_log(text):
    print('{}: {}'.format(DTConvert().dtstring, text))
