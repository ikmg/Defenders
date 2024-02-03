from database import KeepedReport
from backend import create_import_protocol, create_init_protocol, create_result_file
from tools import DateTimeConvert


class RecordCount:
    """Суммарные количественные показатели импорта"""

    def __init__(self):
        self.total = 0  # всего персон в файле
        self.on_send = 0  # подходит для отправки
        self.sended = 0  # отправлено
        self.answered = 0  # получено ответов


class ImportData:
    """Информация об импорте"""

    def __init__(self, app):
        self.app = app
        self.model = None
        self.record_count = RecordCount()

    @property
    def session(self):
        return self.app.database.session

    def __repr__(self):
        return '{} <{}>, записей: всего - {}, на отправку - {}, отправлено - {}, ответов - {}'.format(
            self.model.eskk_military_subject.short_name,
            self.model.id,
            self.record_count.total,
            self.record_count.on_send,
            self.record_count.sended,
            self.record_count.answered
        )

    def get_import(self, import_id):
        self.model = self.session.query(KeepedReport)
        self.model = self.model.filter(KeepedReport.id == import_id)
        self.model = self.model.scalar()
        self.parse_import()

    def parse_import(self):
        """Подсчет количественных показателей импорта"""
        if self.model:
            # всего
            self.record_count.total = len(self.model.keeped_report_records)
            for record in self.model.keeped_report_records:
                # записей на отправку
                if record.critical_messages == '' and record.is_find_in_orders:
                    self.record_count.on_send += 1
                # записей отправлено
                if record.provided_report_record:
                    self.record_count.sended += 1
                # получено ответов
                if record.provided_report_record:
                    if record.provided_report_record.answer_init:
                        self.record_count.answered += 1
            # Обманка интерфейса с количеством записей первых отправок (отправлено больше чем подходит на отправку)
            if self.record_count.sended > self.record_count.on_send:
                self.record_count.on_send = self.record_count.sended

    def table_model_row(self):
        return [
            DateTimeConvert(self.model.created_utc).string,  # должно быть дата/время
            self.model.id,
            self.model.eskk_military_subject.short_name,
            self.record_count.total,
            self.record_count.on_send,
            self.record_count.sended,
            self.record_count.answered,
            self.model.contact_info,
            self.model.is_finished
        ]

    def create_import_protocol(self):
        subject_dir = self.app.storage.imports.add_dir(self.model.eskk_military_subject_id)
        destination = subject_dir.add_file('{}_import.xlsx'.format(self.model.id))
        create_import_protocol(self.session, self.model.id, destination)
        destination.start()

    def create_init_protocol(self):
        subject_dir = self.app.storage.imports.add_dir(self.model.eskk_military_subject_id)
        destination = subject_dir.add_file('{}_init.xlsx'.format(self.model.id))
        create_init_protocol(self.session, self.model.id, destination)
        destination.start()

    def create_result_file(self):
        create_result_file(self.session, self.model.id, self.result_file)
        self.result_file.start()

    def finish_work(self):
        """Поставить/снять отметку о завершении работы с импортом"""
        if self.model:
            self.model.is_finished = not self.model.is_finished
            self.session.commit()

    def delete_import(self):
        """Удаление импорта"""
        # TODO сделать удаление файла
        for record in self.model.keeped_report_records:
            self.session.delete(record)
        self.session.delete(self.model)
        self.session.commit()

    @property
    def is_can_make_result(self):
        """Можно ли завершить работу с импортом"""
        count = self.record_count
        if self.model and count.sended == count.answered and count.sended >= count.on_send:
            return True
        else:
            return False

    @property
    def is_can_delete(self):
        """Можно ли удалить сведения об импорте"""
        if self.record_count.sended == 0 and self.record_count.answered == 0:
            return True
        else:
            return False

    @property
    def original_file(self):
        return self.app.root.add_file(self.model.instance_filename)
        # File(self.model.instance_filename)

    @property
    def result_file(self):
        return self.original_file.dir.add_file(
            '{}_result.xlsx'.format(self.model.id)
        )


class ImportsListData:

    def __init__(self, app):
        self.app = app
        self.rows = []
        # self.records_count = RecordCount()
        # self.unique_subjects = set()
        # self.period = {'min': None, 'max': None}
        # self.total_finished = 0

    @property
    def session(self):
        return self.app.database.session

    def get_data(self):
        models = self.session.query(KeepedReport)
        models = models.order_by(KeepedReport.created_utc.desc())
        models = models.all()
        zero_count = len(str(len(models)))
        for index, model in enumerate(models):
            imported = ImportData(self.app)
            imported.model = model
            imported.parse_import()

            # self.unique_subjects.add(imported.model.eskk_military_subject_id)
            # self.records_count.total += imported.record_count.total
            # self.records_count.sended += imported.record_count.sended
            # self.records_count.on_send += imported.record_count.on_send
            # self.records_count.answered += imported.record_count.answered
            #
            # if not self.period['min'] and not self.period['max']:
            #     self.period['min'] = imported.model.created_utc
            #     self.period['max'] = imported.model.created_utc
            #
            # if imported.model.created_utc < self.period['min']:
            #     self.period['min'] = imported.model.created_utc
            #
            # if imported.model.created_utc > self.period['max']:
            #     self.period['max'] = imported.model.created_utc
            #
            # if imported.model.is_finished:
            #     self.total_finished += 1

            self.rows.append([str(index + 1).zfill(zero_count)] + imported.table_model_row())
        # self.rows.append(self.total_row())
        return self.rows

    # @property
    # def period_days(self):
    #     if self.period['max'] and self.period['min']:
    #         return (self.period['max'] - self.period['min']).days
    #     else:
    #         # если нет записей в БД
    #         return 0

    # def total_row(self):
    #     return [
    #         'ИТОГО',
    #         '{} дня(ей)'.format(self.period_days),
    #         '{} файла(ов)'.format(len(self.rows)),
    #         '{} субъекта(ов)'.format(len(self.unique_subjects)),
    #         self.records_count.total,
    #         self.records_count.on_send,
    #         self.records_count.sended,
    #         self.records_count.answered,
    #         'Справочно: не отправлено {}, нет ответов {}'.format(
    #             self.records_count.on_send - self.records_count.sended,
    #             self.records_count.sended - self.records_count.answered
    #         ),
    #         self.total_finished
    #     ]
