from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush

from .base_tv import TableView

from database import EskkMilitarySubject, KeepedReport


class ImportSubjectsTableView(TableView):

    def __init__(self, app):
        self.app = app
        super().__init__(self.app.database.session)
        self.headers = ['number', 'subject', 'files', 'finished', 'persons', 'on_send', 'sended', 'answered', 'status']
        self.description = ['№', 'Субъект', 'Файлов', 'Завершено', 'Персон', 'К отправке', 'Отправлено', 'Ответов', 'Статус']
        self.get_data()

    def get_data(self):
        report = []
        total = {
                'subject': 'ИТОГО:',
                'files': 0,
                'finished': 0,
                'persons': 0,
                'on_send': 0,
                'sended': 0,
                'answered': 0
            }
        models = self.session.query(EskkMilitarySubject).order_by(EskkMilitarySubject.created_utc).all()
        for model in models:
            report.append({
                'id': model.id,
                'subject': model.short_name,
                'files': 0,
                'finished': 0,
                'persons': 0,
                'on_send': 0,
                'sended': 0,
                'answered': 0
            })

        models = self.session.query(KeepedReport).all()
        for model in models:
            for subject in report:
                if subject['id'] == model.eskk_military_subject_id:
                    subject['files'] += 1
                    subject['finished'] += 1 if model.is_finished else 0
                    subject['persons'] += len(model.keeped_report_records)
                    for record in model.keeped_report_records:
                        if record.critical_messages == '' and record.is_find_in_orders:
                            subject['on_send'] += 1
                        if record.provided_report_record:
                            subject['sended'] += 1
                            if record.provided_report_record.answer_init:
                                subject['answered'] += 1

        number = 0
        for row in report:
            if row['files'] > 0:
                number += 1

                if row['files'] == row['finished']:
                    status = 'Полностью завершено'
                elif row['sended'] > row['answered']:
                    status = 'В работе (не все ответы поступили)'
                elif row['sended'] == row['answered']:
                    status = 'Можно завершить работу c {} загрузками'.format(row['files'] - row['finished'])
                else:
                    status = 'Интересный статус'

                # Обманка интерфейса с количеством записей первых отправок (отправлено больше чем подходит на отправку)
                if row['sended'] > row['on_send']:
                    row['on_send'] = row['sended']

                self._data_.append([
                    number,
                    row['subject'],
                    row['files'],
                    row['finished'],
                    row['persons'],
                    row['on_send'],
                    row['sended'],
                    row['answered'],
                    status
                ])
                total['files'] += row['files']
                total['finished'] += row['finished']
                total['persons'] += row['persons']
                total['on_send'] += row['on_send']
                total['sended'] += row['sended']
                total['answered'] += row['answered']
        self._data_.append([
            number + 1,
            total['subject'],
            total['files'],
            total['finished'],
            total['persons'],
            total['on_send'],
            total['sended'],
            total['answered']
        ])


class ImportCountTableView(TableView):

    def __init__(self, app):
        self.app = app
        super().__init__(self.app.database.session)
        self.headers = ['name', 'value']
        self.description = ['Показатель', 'Значение']
        self.get_data()

    def data(self, index, role=Qt.DisplayRole):
        try:
            value = self._data_[index.row()][index.column()]
        except IndexError:
            value = ''

        if role == Qt.DisplayRole:
            return value
        elif role == Qt.BackgroundRole:
            if self._data_[index.row()][1] == '':
                return QBrush(Qt.darkGray)
            else:
                return QBrush(Qt.gray)

    def get_data(self):
        result = {
            'imports': {'name': 'Загружено всего (за все время)', 'count': 0},
            'finished': {'name': 'Отмечены как завершенные', 'count': 0},
            'period': {'name': 'С момента первой загрузки (дней)', 'min': None, 'max': None, 'delta': None},
            'subjects': {'name': 'Уникальных субъектов', 'unique': set()},
            'persons': {'name': 'Загружено всего (за все время)', 'count': 0},
            'on_send': {'name': 'Передано на отправку', 'count': 0},
            'sended': {'name': 'Отправлено', 'count': 0},
            'answered': {'name': 'Поступило ответов', 'count': 0}
        }

        models = self.session.query(KeepedReport)
        models = models.order_by(KeepedReport.created_utc.desc())
        models = models.all()

        for model in models:
            result['imports']['count'] += 1
            result['finished']['count'] += 1 if model.is_finished else 0
            result['subjects']['unique'].add(model.eskk_military_subject_id)
            result['persons']['count'] += len(model.keeped_report_records)

            correction_on_send = 0
            correction_sended = 0

            for record in model.keeped_report_records:
                # записей на отправку
                if record.critical_messages == '' and record.is_find_in_orders:
                    correction_on_send +=1
                # записей отправлено
                if record.provided_report_record:
                    correction_sended += 1
                # получено ответов
                if record.provided_report_record:
                    if record.provided_report_record.answer_init:
                        result['answered']['count'] += 1

            if not result['period']['min'] and not result['period']['max']:
                result['period']['min'] = model.created_utc
                result['period']['max'] = model.created_utc
            elif model.created_utc < result['period']['min']:
                result['period']['min'] = model.created_utc
            elif model.created_utc > result['period']['max']:
                result['period']['max'] = model.created_utc

            # коррекция для первых выгрузок
            result['sended']['count'] += correction_sended
            if correction_sended > correction_on_send:
                result['on_send']['count'] += correction_sended
            else:
                result['on_send']['count'] += correction_on_send

        self._data_.append(['Файлы', ''])
        self._data_.append([result['imports']['name'], result['imports']['count']])
        self._data_.append([result['finished']['name'], result['finished']['count']])
        self._data_.append(['Продолжительность', ''])
        self._data_.append([result['period']['name'], self.period_days(result['period']['min'], result['period']['max'])])
        self._data_.append(['Субъекты', ''])
        self._data_.append([result['subjects']['name'], len(result['subjects']['unique'])])
        self._data_.append(['Персоны', ''])
        self._data_.append([result['persons']['name'], result['persons']['count']])
        self._data_.append([result['on_send']['name'], result['on_send']['count']])
        self._data_.append([result['sended']['name'], result['sended']['count']])
        self._data_.append([result['answered']['name'], result['answered']['count']])
        self._data_.append(['Справка', ''])
        self._data_.append(['Не отправлено персон', result['on_send']['count'] - result['sended']['count']])
        self._data_.append(['Нет ответов по персонам', result['sended']['count'] - result['answered']['count']])

    def period_days(self, min, max):
        if min and max:
            return (max - min).days
        else:
            # если нет записей в БД
            return 0
