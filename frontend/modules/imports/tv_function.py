import operator

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QBrush

from .dialog import DialogImport
from .tv_data import ImportData, ImportsListData


class ImportsTableViewer:

    def __init__(self, main):
        self.main = main
        self.main.tableView_imports.setSortingEnabled(True)
        self.main.tableView_imports.doubleClicked.connect(self.open_dialog_import)
        self.get_table_content()

    def get_table_content(self):
        table_model = ImportsTableModel(self.main.app)
        self.main.tableView_imports.setModel(table_model)
        self.main.tableView_imports.resizeColumnsToContents()

    def selected_import(self):
        import_id = self.main.tableView_imports.currentIndex().siblingAtColumn(2).data(Qt.DisplayRole)
        import_item = ImportData(self.main.app)
        import_item.get_import(import_id)
        return import_item

    def open_dialog_import(self):
        import_item = self.selected_import()
        dialog = DialogImport(self.main.app, import_item)
        dialog.exec()
        self.get_table_content()


class ImportsTableModel(QAbstractTableModel):

    def __init__(self, app):
        super(QAbstractTableModel, self).__init__()
        self.headers = [
            'index',
            'created_utc',
            'id',
            'subject_name',
            'total',
            'on_send',
            'sended',
            'answered',
            'contact_info',
            'is_finished'
        ]
        self.description = [
            '№',
            'Дата/время',
            'Номер импорта',
            'Наименование субъекта войск',
            'Всего',
            'К отправке',
            'Отправлено',
            'Ответов',
            'Отправитель',
            'Завершено'
        ]
        self._data_ = ImportsListData(app).get_data()  # отображаемые записи в таблице

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
        elif role == Qt.BackgroundRole:
            on_send = self._data_[index.row()][5]
            sended = self._data_[index.row()][6]
            answered = self._data_[index.row()][7]
            # if self._data_[index.row()][0] == 'ИТОГО':
            #     return QBrush(Qt.darkRed)
            if self._data_[index.row()][9]:
                return QBrush(Qt.darkGray)
            elif sended == answered and sended >= on_send:
                return QBrush(Qt.darkGreen)
            elif sended > answered:
                return QBrush(Qt.darkYellow)

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
