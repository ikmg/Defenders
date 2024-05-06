from database import KeepedReport
from backend import create_import_protocol, create_init_protocol, create_result_file
from tools import DTConvert


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
            DTConvert(self.model.created_utc).dtstring,  # должно быть дата/время
            self.model.id,
            self.model.eskk_military_subject.short_name,
            self.record_count.total,
            self.record_count.on_send,
            self.record_count.sended,
            self.record_count.answered,
            self.model.contact_info,
            self.model.is_finished
        ]

    def dialog_table_model_rows(self):
        result = []
        for record in self.model.keeped_report_records:
            row = [
                record.file_row_num,
                record.linked_defender.linked_person.person_appeal,
                record.linked_defender.picked_personal_number.value,
                # record.linked_defender.picked_military_subject.value,
                record.critical_messages,
                record.warning_messages,
                record.provided_report_record.provided_report_id if record.provided_report_record else 'Нет',
                record.provided_report_record.answer_init.comment if record.provided_report_record and record.provided_report_record.answer_init else 'Нет',
            ]
            result.append(row)
        return result

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

    @property
    def result_file(self):
        return self.original_file.dir.add_file(
            '{}_result.xlsx'.format(self.model.id)
        )


class ImportsListData:

    def __init__(self, app):
        self.app = app
        self.rows = []

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
            self.rows.append([str(index + 1).zfill(zero_count)] + imported.table_model_row())
        return self.rows
