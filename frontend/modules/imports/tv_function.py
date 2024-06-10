import operator

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QBrush, QIcon, QGuiApplication
from PyQt5.QtWidgets import QAction, QMessageBox

from .dialog import DialogImport
from .import_item import ImportItem
from .tv_data import ImportData, ImportsListData


class ImportsTableViewer:

    def __init__(self, main):
        self.main = main
        self.main.tableView_imports.setSortingEnabled(True)
        self.main.tableView_imports.doubleClicked.connect(self.open_dialog_import)
        self.init_context_menu()
        self.get_table_content()

    def get_table_content(self):
        table_model = ImportsTableModel(self.main.app)
        self.main.tableView_imports.setModel(table_model)
        self.main.tableView_imports.resizeColumnsToContents()

    def selected_import_data(self):
        import_id = self.main.tableView_imports.currentIndex().siblingAtColumn(2).data(Qt.DisplayRole)
        import_data = ImportData(self.main.app)
        import_data.get_import(import_id)
        return import_data

    def selected_import_item(self):
        return ImportItem(self.main, self.selected_import_data())

    def open_dialog_import(self):
        dialog = DialogImport(self.main.app, self.selected_import_data())
        dialog.exec()
        self.get_table_content()

    def init_context_menu(self):
        self.main.tableView_imports.setContextMenuPolicy(Qt.ActionsContextMenu)

        copy_contacts = QAction(self.main.tableView_imports)
        copy_contacts.setText('Копировать контакт в буфер...')
        copy_contacts.triggered.connect(self.copy_contacts)

        received_file = QAction(self.main.tableView_imports)
        received_file.setText('Поступивший файл')
        received_file.setIcon(QIcon(self.main.app.storage.images.open.path))
        received_file.triggered.connect(self.open_received_file)

        protocol_import = QAction(self.main.tableView_imports)
        protocol_import.setText('Протокол импорта')
        protocol_import.setIcon(QIcon(self.main.app.storage.images.import_p.path))
        protocol_import.triggered.connect(self.open_protocol_import)

        protocol_identify = QAction(self.main.tableView_imports)
        protocol_identify.setText('Протокол идентификации')
        protocol_identify.setIcon(QIcon(self.main.app.storage.images.init_p.path))
        protocol_identify.triggered.connect(self.open_protocol_init)

        separator1 = QAction(self.main.tableView_imports)
        separator1.setSeparator(True)

        separator2 = QAction(self.main.tableView_imports)
        separator2.setSeparator(True)

        result_file = QAction(self.main.tableView_imports)
        result_file.setText('Результирующий файл')
        result_file.setIcon(QIcon(self.main.app.storage.images.result.path))
        result_file.triggered.connect(self.create_result_file)

        import_finished = QAction(self.main.tableView_imports)
        import_finished.setText('Завершить')
        import_finished.setIcon(QIcon(self.main.app.storage.images.finish.path))
        import_finished.triggered.connect(self.finish_work)

        delete_file = QAction(self.main.tableView_imports)
        delete_file.setText('Удалить')
        delete_file.setIcon(QIcon(self.main.app.storage.images.delete.path))
        delete_file.triggered.connect(self.delete_import)

        self.main.tableView_imports.addAction(copy_contacts)
        self.main.tableView_imports.addAction(separator1)
        self.main.tableView_imports.addAction(received_file)
        self.main.tableView_imports.addAction(protocol_import)
        self.main.tableView_imports.addAction(protocol_identify)
        self.main.tableView_imports.addAction(separator2)
        self.main.tableView_imports.addAction(result_file)
        self.main.tableView_imports.addAction(import_finished)
        self.main.tableView_imports.addAction(delete_file)

    def copy_contacts(self):
        import_item = self.selected_import_item()
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(import_item.import_data.model.contact_info)

    def open_received_file(self):
        import_item = self.selected_import_item()
        import_item.open_received_file()

    def open_protocol_import(self):
        import_item = self.selected_import_item()
        import_item.open_protocol_import()

    def open_protocol_init(self):
        import_item = self.selected_import_item()
        import_item.open_protocol_init()

    def create_result_file(self):
        import_item = self.selected_import_item()
        if import_item.import_data.is_can_make_result:
            import_item.create_result_file()
        else:
            QMessageBox.warning(self.main, 'Результирующий файл', 'Невозможно создать результирующий файл')

    def finish_work(self):
        import_item = self.selected_import_item()
        if import_item.import_data.is_can_make_result:
            import_item.finish_work()
            self.get_table_content()
        else:
            QMessageBox.critical(self.main, 'Завершение работы', 'Невозможно завершить работу с файлом')

    def delete_import(self):
        import_item = self.selected_import_item()
        if import_item.import_data.is_can_delete:
            import_item.delete_import()
            self.get_table_content()
        else:
            QMessageBox.critical(self.main, 'Удаление загрузки', 'Невозможно удалить загрузку')


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
