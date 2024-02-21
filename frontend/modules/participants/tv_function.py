import operator

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QAction

from .tv_data import ParticipantsListData, ParticipantData


class ParticipantsTableViewer:

    def __init__(self, main):
        self.main = main
        self.main.tableView_order_persons.setSortingEnabled(True)
        self.main.lineEdit_find_order_person.returnPressed.connect(self.get_table_content)
        self.init_context_menu()
        self.get_table_content()

    def init_context_menu(self):
        self.main.tableView_order_persons.setContextMenuPolicy(Qt.ActionsContextMenu)

        person_periods = QAction(self.main.tableView_order_persons)
        person_periods.setText('Периоды персоны')
        person_periods.setIcon(QIcon(self.main.app.storage.images.info.path))
        person_periods.triggered.connect(self.person_periods)

        fio_periods = QAction(self.main.tableView_order_persons)
        fio_periods.setText('Периоды по ФИО')
        fio_periods.setIcon(QIcon(self.main.app.storage.images.result.path))
        fio_periods.triggered.connect(self.fio_periods)

        self.main.tableView_order_persons.addAction(person_periods)
        self.main.tableView_order_persons.addAction(fio_periods)

    def get_table_content(self):
        table_model = ParticipantsTableModel(self.main.app, self.main.lineEdit_find_order_person.text())
        self.main.tableView_order_persons.setModel(table_model)
        self.main.tableView_order_persons.resizeColumnsToContents()
        if self.main.lineEdit_find_order_person.text():
            QMessageBox.information(self.main, 'Результат', 'Найдено {} записей'.format(len(table_model._data_)))

    def selected_item(self):
        participant_id = self.main.tableView_order_persons.currentIndex().siblingAtColumn(0).data(Qt.UserRole)
        participant_item = ParticipantData(self.main.app)
        participant_item.get_participant(participant_id)
        return participant_item

    def person_periods(self):
        participant_item = self.selected_item()
        QMessageBox.information(self.main, 'Периоды участия', participant_item.person_periods())

    def fio_periods(self):
        participant_item = self.selected_item()
        QMessageBox.information(self.main, 'Периоды участия', participant_item.fio_periods())


class ParticipantsTableModel(QAbstractTableModel):

    def __init__(self, app, filter_text=None):
        super(QAbstractTableModel, self).__init__()
        self.headers = ['number', 'rank', 'fio', 'personal_number', 'subject']
        self.description = ['№', 'Звание', 'Фамилия, имя, отчество', 'Личный номер', 'Субъект']
        self._data_ = ParticipantsListData(app).get_data(filter_text)  # отображаемые записи в таблице

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.layoutAboutToBeChanged.emit()
        self._data_ = sorted(self._data_, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self._data_.reverse()
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data_[index.row()][index.column()]
        elif role == Qt.UserRole:
            # print(index.row(), index.column())
            return self._data_[index.row()][5]

        # try:
        #     value = self._data_[index.row()][index.column()]
        # except IndexError:
        #     value = ''
        # if role == Qt.DisplayRole:
        #     return value
        # elif role == Qt.UserRole:
        #     return self._data_[index.row()][5]

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
