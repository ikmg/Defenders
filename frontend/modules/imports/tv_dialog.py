import operator

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex


class DialogTableModel(QAbstractTableModel):

    def __init__(self, rows):
        super(QAbstractTableModel, self).__init__()
        self.headers = [
            'row_num',
            'person_appeal',
            'personal_number',
            # 'picked_subject',
            'critical_messages',
            'warning_messages',
            'is_sended',
            'answer'
        ]
        self.description = [
            'Строка',
            'ФИО',
            'Личный номер',
            # 'Место службы',
            'Критические ошибки',
            'Предупреждения',
            'Отправлен',
            'Ответ СФР'
        ]
        self._data_ = rows

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.layoutAboutToBeChanged.emit()
        self._data_ = sorted(self._data_, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self._data_.reverse()
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        try:
            value = self._data_[index.row()][index.column()]
        except IndexError:
            value = ''
        if role == Qt.DisplayRole:
            return value

    def rowCount(self, parent=QModelIndex()):
        return len(self._data_)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.description[section]
        return

    def column_name(self, header_index):
        return self.description[header_index]
