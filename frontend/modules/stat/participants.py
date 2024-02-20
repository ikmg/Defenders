from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from sqlalchemy import or_

from database import LinkedOrderPerson, KeepedOrderRecord
from .base_tv import TableView
from tools import DTConvert


def category(pn: str):
    if 'А' in pn or 'A' in pn:
        key = 'A'
    elif 'ПР' in pn or 'ПP' in pn:
        key = 'PR'
    elif 'РС' in pn or 'РC' in pn or 'PС' in pn or 'PC' in pn:
        key = 'RS'
    else:
        key = 'unknown'
    return key


class Count:

    def __init__(self):
        self.count = 0
        self.A = 0
        self.PR = 0
        self.RS = 0
        self.unknown = 0

    def __repr__(self):
        return '{} - {}'.format(self.count, self.is_ok)

    def add(self, key: str):
        self.count += 1
        if key == 'A':
            self.A += 1
        elif key == 'PR':
            self.PR += 1
        elif key == 'RS':
            self.RS += 1
        elif key == 'unknown':
            self.unknown += 1

    def percent_a(self):
        return '{}%'.format(round(self.A/self.count*100, 2))

    def percent_pr(self):
        return '{}%'.format(round(self.PR/self.count*100, 2))

    def percent_rs(self):
        return '{}%'.format(round(self.RS/self.count*100, 2))

    def percent_unk(self):
        return '{}%'.format(round(self.unknown/self.count*100, 2))

    def tv(self):
        result = []
        result.append(['Количество', self.count, 'в том числе'])
        result.append(['Офицеры', self.A, self.percent_a()])
        result.append(['Прапорщики', self.PR, self.percent_pr()])
        result.append(['Солдаты/сержанты', self.RS, self.percent_rs()])
        if self.unknown > 0:
            result.append(['Не установлено', self.unknown, self.percent_unk()])
        return result

    @property
    def is_ok(self):
        return True if self.count == self.A + self.PR + self.RS + self.unknown else False


class Persons:

    def __init__(self):
        self.models = 0
        self.total = Count()
        self.departure = {}
        self.unknown_list = []

    def add_person(self, pn: str, key: str):
        self.total.add(key)
        if key == 'unknown':
            self.unknown_list.append(pn)

    def add_year(self, year: int):
        if year not in self.departure:
            self.departure[year] = Count()

    @property
    def is_ok(self):
        return True if self.models == self.total.count else False


class Periods:

    def __init__(self):
        self.models = 0
        self.total = Count()
        self.years = {}
        self.unknown_years = Count()
        self.unknown = []

    def add_year(self, year: int):
        if year not in self.years:
            self.years[year] = Count()

    def add_unknown(self, begin: str, end: str):
        self.unknown.append('c <{}> по <{}>'.format(begin, end))

    @property
    def is_ok(self):
        sum = len(self.unknown)
        is_ok = True
        for year in self.years:
            sum += self.years[year].count
            is_ok *= self.years[year].is_ok
        return True if self.models == self.total.count and self.models == sum and is_ok else False


class Participants:

    def __init__(self, models):
        self.persons = Persons()
        self.periods = Periods()

        self.persons.models = len(models)
        print(DTConvert().dtstring, '{} участников'.format(self.persons.models))
        for index, model in enumerate(models):
            if (index + 1) % 10000 == 0:
                print(DTConvert().dtstring, 'обработано {}'.format(index + 1))
            key = category(model.picked_personal_number.value)
            self.persons.add_person(model.picked_personal_number.value, key)
            self.periods.models += len(model.linked_order_person_periods)
            current_person_years = set()
            for period in model.linked_order_person_periods:
                date = DTConvert(period.date_begin).date
                if date:
                    year = date.year
                    self.persons.add_year(year)
                    current_person_years.add(year)
                    self.periods.add_year(year)
                    self.periods.years[year].add(key)
                else:
                    self.periods.unknown_years.add(key)
                    self.periods.add_unknown(period.date_begin, period.date_end)
                self.periods.total.add(key)
            for year in current_person_years:
                self.persons.departure[year].add(key)

    def tv(self):
        result = []
        result.append(['УЧАСТНИКИ', '', ''])
        result.append(['', 'Всего', ''])
        result = result + self.persons.total.tv()
        result.append(['Список неустановленных', ', '.join(self.persons.unknown_list), ''])
        result.append(['', 'По выездам', ''])
        self.persons.departure = dict(sorted(self.persons.departure.items()))
        for year in self.persons.departure:
            result.append(['', '{} год'.format(year), ''])
            result = result + self.persons.departure[year].tv()
        result.append(['ВЫЕЗДЫ', '', ''])
        result.append(['', 'Всего', ''])
        result = result + self.periods.total.tv()
        result.append(['', 'По годам', ''])
        self.periods.years = dict(sorted(self.periods.years.items()))
        for year in self.periods.years:
            result.append(['', '{} год'.format(year), ''])
            result = result + self.periods.years[year].tv()
        result.append(['', 'Год не установлен', ''])
        result = result + self.periods.unknown_years.tv()
        return result


class ParticipantsTableView(TableView):

    def __init__(self, app):
        self.app = app
        super().__init__(self.app.database.session)
        self.headers = ['name', 'value', 'percent']
        self.description = ['Показатель', 'Значение', 'Соотношение']
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
                return QBrush(Qt.darkYellow)
            elif self._data_[index.row()][0] == '':
                return QBrush(Qt.darkGray)
            else:
                return QBrush(Qt.gray)

    def get_data(self):
        print(DTConvert().dtstring, 'Анализ участников и периодов')
        models = self.session.query(LinkedOrderPerson).all()
        participants = Participants(models)
        self._data_ = participants.tv()


class ParticipantsErrorsTableView(TableView):

    def __init__(self, app):
        self.app = app
        super().__init__(self.app.database.session)
        self.headers = ['row_num', 'warning', 'critical']
        self.description = ['Номер строки', 'Предупреждение', 'Критическая ошибка']
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
                return QBrush(Qt.darkRed)
            elif self._data_[index.row()][2] == '':
                return QBrush(Qt.darkYellow)

    def get_data(self):
        models = self.session.query(KeepedOrderRecord)
        models = models.filter(or_(KeepedOrderRecord.critical_messages != '', KeepedOrderRecord.warning_messages != ''))
        models = models.order_by(KeepedOrderRecord.file_row_num).all()
        for model in models:
            self._data_.append([model.file_row_num, model.warning_messages, model.critical_messages])
