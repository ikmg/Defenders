from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from sqlalchemy import or_, desc

from database import KeepedOrderRecord, OrdersStat, KeepedOrder
from .base_tv import TableView


class ParticipantsTableView(TableView):

    def __init__(self, app):
        self.app = app
        super().__init__(self.app.database.session)
        self.headers = ['data_type', 'name', 'count', 'A', 'PR', 'RS', 'other', 'note']
        self.description = ['Раздел', 'Сведения', 'Всего', 'Офицеры', 'Прапорщики', 'Сержанты/Солдаты', 'Другие', 'Примечание']
        self.get_data()

    def data(self, index, role=Qt.DisplayRole):
        try:
            value = self._data_[index.row()][index.column()]
        except IndexError:
            value = ''

        if role == Qt.DisplayRole:
            return value
        elif role == Qt.BackgroundRole:
            if 'Сводные' in self._data_[index.row()][1]:
                return QBrush(Qt.darkGray)
            else:
                return QBrush(Qt.gray)

    def get_data(self):
        order = self.session.query(KeepedOrder).order_by(desc(KeepedOrder.created_utc)).limit(1).scalar()
        if order:
            models = self.session.query(OrdersStat).filter(OrdersStat.keeped_order_id == order.id).order_by(OrdersStat.sort).all()
            for model in models:
                self._data_.append([
                    model.data_type,
                    model.name,
                    model.count,
                    '{} ({}%)'.format(model.A, model.A_percent),
                    '{} ({}%)'.format(model.PR, model.PR_percent),
                    '{} ({}%)'.format(model.RS, model.RS_percent),
                    '{} ({}%)'.format(model.other, model.other_percent),
                    model.note
                ])


class ParticipantsErrorsTableView(TableView):

    def __init__(self, app):
        self.app = app
        super().__init__(self.app.database.session)
        self.headers = ['row_num', 'warning', 'critical']
        self.description = ['Строка', 'Предупреждение', 'Критическая ошибка']
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
