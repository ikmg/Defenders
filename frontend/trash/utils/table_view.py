from abc import abstractmethod

from PyQt5.QtGui import QBrush
from sqlalchemy import or_
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from sqlalchemy.sql.operators import ilike_op

from database import KeepedReport, LinkedOrderPerson, PickedLastName, PickedFirstName, PickedMiddleName, LinkedOrderFIO, LinkedDefender, LinkedPerson, ProvidedReport, \
    EskkMilitarySubject, PickedPersonalNumber
from frontend.trash.table_views.data.tv_import import ImportsUI
from tools.date_time import DateTimeConvert


class TableView(QAbstractTableModel):

    def __init__(self, session):
        super(QAbstractTableModel, self).__init__()
        self.session = session
        self.description = []  # наименования столбцов в кириллице
        self.headers = []  # наименования столбцов в латинице
        self._data_ = []  # отображаемые записи в таблице

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.description[section]
        return

    def data(self, index, role=Qt.DisplayRole):
        try:
            value = self._data_[index.row()][index.column()]
        except IndexError:
            value = ''

        if role == Qt.DisplayRole:
            if isinstance(value, bool):
                if value:
                    return 'ДА'
                else:
                    return 'НЕТ'
            else:
                return value

    def rowCount(self, parent=QModelIndex()):
        return len(self._data_)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def column_name(self, header_index):
        return self.description[header_index]

    @abstractmethod
    def get_data(self):
        pass


class ImportsTableView(TableView):

    def __init__(self, app):
        self.app = app
        super().__init__(self.app.database.session)
        self.headers = [
            'index',
            'created_utc',
            'id',
            'subject_name',
            'records_total',
            'records_on_send',
            'records_sended',
            'records_answered',
            'contact_info',
            'is_finished'
        ]
        self.description = [
            '№',
            'Дата/время загрузки',
            'Рег. номер импорта',
            'Наименование субъекта войск',
            'Записей всего',
            'На отправку',
            'Отправлено',
            'Ответы СФР',
            'Контакты отправителя',
            'Завершено'
        ]
        self.get_data()

    def get_data(self):
        imports = ImportsUI(self.app)
        self._data_ = imports.get_data()

    def data(self, index, role=Qt.DisplayRole):
        value = super().data(index)
        if role == Qt.DisplayRole:
            return value
        elif role == Qt.BackgroundRole:
            on_send = self._data_[index.row()][5]
            sended = self._data_[index.row()][6]
            answered = self._data_[index.row()][7]

            if self._data_[index.row()][0] == 'ИТОГО':
                return QBrush(Qt.darkRed)
            elif self._data_[index.row()][9]:
                return QBrush(Qt.darkGray)
            elif sended == answered and sended >= on_send:
                return QBrush(Qt.darkGreen)
            elif sended > answered:
                return QBrush(Qt.darkYellow)


class ExportTableView(TableView):

    def __init__(self, session):
        super().__init__(session)
        self.headers = ['number', 'id', 'created_utc', 'records_count', 'protocol', 'answer']
        self.description = ['№', 'Регистрационный номер', 'Дата/время', 'Количество', 'Протокол загрузки', 'Ответ СФР']
        self.get_data()

    def get_data(self):
        summary = 0
        answer_count = 0
        models = self.session.query(ProvidedReport)
        models = models.order_by(ProvidedReport.created_utc.desc())
        models = models.all()
        for index, model in enumerate(models):
            answer = '---'
            if model.answer_import:
                answer_count += 1
                answer = model.answer_import.result
            row = [
                index + 1,
                model.id,
                DateTimeConvert(model.created_utc).string,  # должно быть дата/время
                len(model.provided_report_records),
                model.answer_import.reg_number if model.answer_import else 'Протокол не поступал',
                answer
            ]
            summary += len(model.provided_report_records)
            self._data_.append(row)
        self._data_.append([
            '---',
            'ИТОГО:',
            '',
            summary,
            '{} из {}'.format(answer_count, len(models))
        ])


class DefendersTableView(TableView):

    def __init__(self, session, filter_text, load=False):
        super().__init__(session)
        self.headers = ['number', 'fio', 'birthday', 'personal_number', 'subject', 'import_id', 'protocol_sfr', 'answer']
        self.description = ['№', 'Фамилия, имя, отчество', 'Дата рождения', 'Личный номер', 'Субъект', 'Рег. номер импорта', 'Протокол СФР', 'Ответ СФР']
        self.filter_text = filter_text
        if load:
            self.get_data()

    def get_data(self):
        parts = self.filter_text.split(' ')

        models = self.session.query(LinkedDefender)
        models = models.join(LinkedPerson)
        models = models.join(PickedLastName)
        models = models.join(PickedFirstName)
        models = models.join(PickedMiddleName)
        models = models.join(PickedPersonalNumber)

        for part in parts:
            if part:
                models = models.filter(
                    or_(
                        # PickedLastName.value.ilike('%{}%'.format(part.lower())),
                        # PickedFirstName.value.ilike('%{}%'.format(part.lower())),
                        # PickedMiddleName.value.ilike('%{}%'.format(part.lower()))

                        ilike_op(PickedLastName.value, '%{}%'.format(part)),
                        ilike_op(PickedFirstName.value, '%{}%'.format(part)),
                        ilike_op(PickedMiddleName.value, '%{}%'.format(part)),
                        ilike_op(PickedPersonalNumber.value, '%{}%'.format(part))
                    )
                )

        models = models.order_by(
            PickedLastName.value,
            PickedFirstName.value,
            PickedMiddleName.value
        )
        models = models.all()

        if models:
            for index, model in enumerate(models):
                # critical = ''
                answer = ''
                prot_sfr = '---'
                import_id = ''
                if model.keeped_report_records:
                    for rec in model.keeped_report_records:
                        # report_id = rec.keeped_report_id
                        # if rec.critical_messages:
                        #     critical = '[{}] {}'.format(report_id, 'критические ошибки')
                        # else:
                        #     critical = '[{}] {}'.format(report_id, 'ОК')
                        if rec.provided_report_record:
                            if rec.provided_report_record.answer_init:
                                answer = 'Ответ СФР: {}'.format(rec.provided_report_record.answer_init.comment)
                                prot_sfr = rec.provided_report_record.provided_report.answer_import.reg_number
                            else:
                                answer = 'Отправлено в СФР, ответ не поступал'
                        else:
                            answer = 'Не отправлено в СФР'
                        import_id = rec.keeped_report_id
                else:
                    answer = '---'

                row = [
                    index + 1,
                    '{} {} {}'.format(
                        model.linked_person.picked_last_name.value,
                        model.linked_person.picked_first_name.value,
                        model.linked_person.picked_middle_name.value
                    ),
                    model.linked_person.birthday,
                    model.picked_personal_number.value,
                    model.picked_military_subject.value,
                    # critical,
                    import_id,
                    prot_sfr,
                    answer
                ]
                self._data_.append(row)
        else:
            self._data_.append(['', 'Уточните критерии поиска', '', '', ''])


class ParticipantsTableView(TableView):

    def __init__(self, session, filter_text, load=False):
        super().__init__(session)
        self.headers = ['rank', 'fio', 'personal_number', 'subject']
        self.description = ['Звание', 'Фамилия, имя, отчество', 'Личный номер', 'Субъект']
        self.filter_text = filter_text
        if load:
            self.get_data()

    def get_data(self):
        parts = self.filter_text.split(' ')

        models = self.session.query(LinkedOrderPerson)
        models = models.join(LinkedOrderFIO)
        models = models.join(PickedLastName)
        models = models.join(PickedFirstName)
        models = models.join(PickedMiddleName)
        models = models.join(PickedPersonalNumber)

        for part in parts:
            if part:
                models = models.filter(
                    or_(
                        PickedLastName.value.ilike('%{}%'.format(part)),
                        PickedFirstName.value.ilike('%{}%'.format(part)),
                        PickedMiddleName.value.ilike('%{}%'.format(part)),
                        PickedPersonalNumber.value.ilike('%{}%'.format(part))
                    )
                )
        models = models.order_by(
            PickedLastName.value,
            PickedFirstName.value,
            PickedMiddleName.value
        )
        models = models.all()
        if models:
            for model in models:
                row = [
                    model.picked_military_rank.value,
                    '{} {} {}'.format(
                        model.linked_order_fio.picked_last_name.value,
                        model.linked_order_fio.picked_first_name.value,
                        model.linked_order_fio.picked_middle_name.value
                    ),
                    model.picked_personal_number.value,
                    model.picked_military_subject.value
                ]
                self._data_.append(row)
        else:
            self._data_.append(['', 'Уточните критерии поиска', '', ''])


class StatImportsTableView(TableView):

    def __init__(self, session):
        super().__init__(session)
        self.headers = ['id', 'subject', 'data', 'persons', 'sended', 'answered']
        self.description = ['ИД', 'Субъект войск', 'Загрузок', 'Защитников', 'Отправлено', 'Ответов']
        self.get_data()

    def get_data(self):
        report = []
        total = {
                'id': '----',
                'path': '----',
                'name': 'ИТОГО:',
                'count': 0,
                'persons': 0,
                'sended': 0,
                'answered': 0
            }
        models = self.session.query(EskkMilitarySubject).order_by(EskkMilitarySubject.created_utc).all()
        for model in models:
            report.append({
                'id': model.id,
                'path': model.path,
                'name': model.short_name,
                'count': 0,
                'persons': 0,
                'sended': 0,
                'answered': 0
            })

        models = self.session.query(KeepedReport).all()
        for model in models:
            for subject in report:
                if subject['id'] == model.eskk_military_subject_id:
                    subject['count'] += 1
                    subject['persons'] += len(model.keeped_report_records)
                    for record in model.keeped_report_records:
                        if record.provided_report_record:
                            subject['sended'] += 1
                            if record.provided_report_record.answer_init:
                                subject['answered'] += 1

        for row in report:
            if row['count'] > 0:
                self._data_.append([
                    row['id'],
                    row['name'],
                    row['count'],
                    row['persons'],
                    row['sended'],
                    row['answered']
                ])
                total['count'] += row['count']
                total['persons'] += row['persons']
                total['sended'] += row['sended']
                total['answered'] += row['answered']
        self._data_.append([
            total['id'],
            total['name'],
            total['count'],
            total['persons'],
            total['sended'],
            total['answered']
        ])
