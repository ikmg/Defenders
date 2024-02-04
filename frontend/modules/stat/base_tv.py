import operator
from abc import abstractmethod

from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel

from backend import csv_from_list


class TableView(QAbstractTableModel):

    def __init__(self, session):
        super(QAbstractTableModel, self).__init__()
        self.session = session
        self.description = []  # наименования столбцов в кириллице
        self.headers = []  # наименования столбцов в латинице
        self._data_ = []  # отображаемые записи в таблице

    def download(self, destination):
        csv_from_list(destination, [self.description] + self._data_)

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.layoutAboutToBeChanged.emit()
        self._data_ = sorted(self._data_, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self._data_.reverse()
        self.layoutChanged.emit()

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
