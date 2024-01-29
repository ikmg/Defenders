from .data import ImportWorkbook, OrderWorkbook, AnswerWorkbook
from .handler import KeepedReportHandler, KeepedOrderHandler

from tools import DateTimeConvert


class ImportUploader:

    def __init__(self, session, subject_id, file_path):
        if not subject_id:
            raise ValueError('не указан субъект войск')
        self.session = session
        self.subject_id = subject_id
        self.workbook = ImportWorkbook(file_path)
        self.import_id = '{}-{}'.format(
            self.subject_id.zfill(4),
            DateTimeConvert().value.strftime('%Y%m%d-%H%M%S')
        )
        self.original_file = None

    def upload(self, destination, contact_info):
        if not contact_info:
            raise ValueError('не указаны контактные данные для обратной связи')
        active_sheet = self.workbook.active
        self.original_file = self.workbook.file
        # TODO копирование происходит до проверки хэш-суммы (исправить наоборот)
        self.workbook.file.copy(destination)
        self.workbook = ImportWorkbook(destination)
        self.workbook.load()
        self.workbook.select_worksheet(active_sheet)
        self.workbook.check_active_worksheet()
        keywords = {
            'import_id': self.import_id,
            'subject_id': self.subject_id,
            'original_filename': self.original_file.path,
            'instance_filename': self.workbook.file.rel_path,
            'hash_sum': self.workbook.file.md5(),
            'contact_info': contact_info,
            'rows_data': self.workbook.worksheet_data()
        }
        KeepedReportHandler(self.session, **keywords)
        # self.session.commit()

    @property
    def storage_filename(self):
        return '{}{}'.format(self.import_id, self.workbook.file.extension)


class OrdersUploader:

    def __init__(self, session, file_path):
        self.session = session
        self.workbook = OrderWorkbook(file_path)
        self.import_id = '{}'.format(DateTimeConvert().value.strftime('%Y%m%d-%H%M%S'))
        self.original_file = None

    def upload(self, destination):
        self.original_file = self.workbook.file
        # TODO копирование происходит до проверки хэш-суммы (исправить наоборот)
        self.workbook.file.copy(destination)
        self.workbook = OrderWorkbook(destination)
        self.workbook.load()
        keywords = {
            'import_id': self.import_id,
            'original_filename': self.original_file.path,
            'workbook': self.workbook
        }
        KeepedOrderHandler(self.session, **keywords)
        # self.session.commit()

    @property
    def storage_filename(self):
        return '{}{}'.format(self.import_id, self.workbook.file.extension)


class AnswerUploader:

    def __init__(self, session, file_path):
        self.session = session
        self.workbook = OrderWorkbook(file_path)
        self.original_file = None