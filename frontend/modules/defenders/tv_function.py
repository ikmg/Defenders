import operator

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtWidgets import QMessageBox

from .tv_data import DefendersListData


class DefendersTableViewer:

    def __init__(self, main):
        self.main = main
        self.main.tableView_defenders.setSortingEnabled(True)
        self.main.lineEdit_find_defender.returnPressed.connect(self.get_table_content)
        self.init_context_menu()
        self.get_table_content()

    def init_context_menu(self):
        pass

    def get_table_content(self):
        table_model = DefendersTableModel(self.main.app, self.main.lineEdit_find_defender.text())
        self.main.tableView_defenders.setModel(table_model)
        self.main.tableView_defenders.resizeColumnsToContents()
        if self.main.lineEdit_find_defender.text():
            QMessageBox.information(self.main, 'Результат', 'Найдено {} записей'.format(len(table_model._data_)))


class DefendersTableModel(QAbstractTableModel):

    def __init__(self, app, filter_text=None):
        super(QAbstractTableModel, self).__init__()
        self.headers = ['number', 'fio', 'birthday', 'personal_number', 'subject', 'import_id', 'protocol_sfr', 'answer']
        self.description = ['№', 'Фамилия, имя, отчество', 'Дата рождения', 'Личный номер', 'Субъект', 'Рег. номер импорта', 'Протокол СФР', 'Ответ СФР']
        self._data_ = DefendersListData(app).get_data(filter_text)  # отображаемые записи в таблице

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

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.description[section]
        return

    def column_name(self, header_index):
        return self.description[header_index]
