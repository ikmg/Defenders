from database import KeepedReport
from backend.download.exporter import defenders_load_data, defenders_identify_data
from tools import DateTimeConvert, File, Directory
from backend.download.wokbooks.xls_file import write_xls_list


class RecordCount:
    """
    Датакласс суммарных количественных показателей загруженного файла
    """

    def __init__(self):
        self.total = 0  # всего персон в файле
        self.on_send = 0  # подходит для отправки
        self.sended = 0  # отправлено
        self.answered = 0  # получено ответов


class ImportUI:
    """
    Класс работы с загруженным файлом (для интерфейса)
    """

    def __init__(self, app):
        """
        :param app: экземпляр класса приложения
        """
        self._app_ = app
        self._session_ = self._app_.database.session
        self.model = None
        self.record_count = RecordCount()

    def __repr__(self):
        return '{} <{}>, записей: всего - {}, на отправку - {}, отправлено - {}, ответов - {}'.format(
            self.model.eskk_military_subject.short_name if self.model else None,
            self.model.id if self.model else None,
            self.record_count.total,
            self.record_count.on_send,
            self.record_count.sended,
            self.record_count.answered
        )

    def get_model(self, import_id):
        """
        Получение модели базы данных
        :param import_id: идентификатор загрузки
        :return: экземпляр класса KeepedReport или None
        """
        self.model = self._session_.query(KeepedReport)
        self.model = self.model.filter(KeepedReport.id == import_id)
        self.model = self.model.scalar()
        self.parse_model()

    def parse_model(self):
        """
        Вычисление суммарных количественных показателей загруженного файла:
        всего, на отправку, отправлено, получено ответов
        :return: None
        """
        if self.model:
            self.record_count.total = len(self.model.keeped_report_records)  # всего
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

    def delete_import(self):
        """
        Удаление сведений о загруженном файле из базы данных
        :return: bool
        """
        try:
            for record in self.model.keeped_report_records:
                self._session_.delete(record)
            self._session_.delete(self.model)
            self._session_.commit()
            return True
        except Exception as e:
            self._session_.rollback()
            print(e.args)
            return False

    def open_original_file(self):
        """
        Открытие поступившего файла
        :return: None
        """
        File(self.original_file_name).start()

    def open_result_file(self):
        """
        Открытие результирующего файла
        :return: None
        """
        File(self.result_file_name).start()

    def create_import_protocol(self):
        """
        Создание и открытие протокола загрузки
        :return: None
        """
        subject_dir = Directory(self._app_.storage.imports.add_dir(self.model.eskk_military_subject_id))
        file = File(subject_dir.add_file('{}_import.xls'.format(self.model.id)))
        write_xls_list(file.path, defenders_load_data(self._app_.database.session, self.model.id))
        file.start()

    def create_init_protocol(self):
        """
        Создание и открытие протокола идентификации
        :return: None
        """
        subject_dir = Directory(self._app_.storage.imports.add_dir(self.model.eskk_military_subject_id))
        file = File(subject_dir.add_file('{}_init.xls'.format(self.model.id)))
        write_xls_list(file.path, defenders_identify_data(self._app_.database.session, self.model.id))
        file.start()

        # filename = self._app_.storage.data.subject_directory(self.model.eskk_military_subject_id)
        # filename = get_new_path(filename, '{}_init.xls'.format(self.model.id))
        # write_xls_list(filename, defenders_identify_data(self._app_.database.session, self.model.id))
        # start_file(filename)

    def finish_work(self):
        """
        Поставить/снять отметку о завершении работы с файлом
        :return: None
        """
        if self.model:
            self.model.is_finished = not self.model.is_finished
            self._session_.commit()

    @property
    def is_can_make_result(self):
        """
        Можно ли завершить работу с файлом
        :return: bool
        """
        count = self.record_count
        if count.sended == count.answered and count.sended >= count.on_send:
            return True
        else:
            return False

    @property
    def is_can_delete(self):
        """
        Можно ли удалить сведения о загрузке файла
        :return: bool
        """
        if self.record_count.sended == 0 and self.record_count.answered == 0:
            return True
        else:
            return False

    @property
    def original_file_name(self):
        return File(self._app_.root.add_file(self.model.instance_filename))

    @property
    def result_file_name(self):
        return File(self.original_file_name.dir.add_file(
            '{}_result{}'.format(self.model.id, self.original_file_name.extension))
        )

    @property
    def table_view_import(self):
        return [
            DateTimeConvert(self.model.created_utc).string if self.model else None,  # должно быть дата/время
            self.model.id if self.model else None,
            self.model.eskk_military_subject.short_name if self.model else None,
            self.record_count.total,
            self.record_count.on_send,
            self.record_count.sended,
            self.record_count.answered,
            self.model.contact_info,
            self.model.is_finished
        ]


class ImportsUI:

    def __init__(self, app):
        self.app = app
        self._session_ = self.app.database.session
        self.data = []
        self.records_count = RecordCount()
        self.unique_subjects = set()
        self.period = {'min': None, 'max': None}
        self.total_finished = 0

    def get_data(self):
        models = self._session_.query(KeepedReport)
        models = models.order_by(KeepedReport.created_utc.desc())
        models = models.all()

        for index, model in enumerate(models):
            imported = ImportUI(self.app)
            imported.model = model
            imported.parse_model()

            self.unique_subjects.add(imported.model.eskk_military_subject_id)
            self.records_count.total += imported.record_count.total
            self.records_count.sended += imported.record_count.sended
            self.records_count.on_send += imported.record_count.on_send
            self.records_count.answered += imported.record_count.answered

            if not self.period['min'] and not self.period['max']:
                self.period['min'] = imported.model.created_utc
                self.period['max'] = imported.model.created_utc

            if imported.model.created_utc < self.period['min']:
                self.period['min'] = imported.model.created_utc

            if imported.model.created_utc > self.period['max']:
                self.period['max'] = imported.model.created_utc

            if imported.model.is_finished:
                self.total_finished += 1

            self.data.append([index + 1] + imported.table_view_import)
        self.data.append(self.total_row())
        return self.data

    @property
    def period_days(self):
        if self.period['max'] and self.period['min']:
            return (self.period['max'] - self.period['min']).days
        else:
            # если нет записей в БД
            return 0

    def total_row(self):
        return [
            'ИТОГО',
            '{} дня(ей)'.format(self.period_days),
            '{} файла(ов)'.format(len(self.data)),
            '{} субъекта(ов)'.format(len(self.unique_subjects)),
            self.records_count.total,
            self.records_count.on_send,
            self.records_count.sended,
            self.records_count.answered,
            'Справочно: не отправлено {}, нет ответов {}'.format(
                self.records_count.on_send - self.records_count.sended,
                self.records_count.sended - self.records_count.answered
            ),
            self.total_finished
        ]
