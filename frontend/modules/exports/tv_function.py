import operator
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QIcon, QBrush
from PyQt5.QtWidgets import QAction, QMessageBox

from tools import File
from .tv_data import ExportData, ExportsListData


class ExportsTableViewer:

    def __init__(self, main):
        self.main = main
        self.main.tableView_exports.setSortingEnabled(True)
        self.init_context_menu()
        self.get_table_content()

    def init_context_menu(self):
        self.main.tableView_exports.setContextMenuPolicy(Qt.ActionsContextMenu)

        export_file = QAction(self.main.tableView_exports)
        export_file.setText('Файл для отправки')
        export_file.setIcon(QIcon(self.main.app.storage.images.import_p.path))
        export_file.triggered.connect(self.create_export_file)
        self.main.tableView_exports.addAction(export_file)

        export_content = QAction(self.main.tableView_exports)
        export_content.setText('Показать первые 10 фамилий')
        export_content.setIcon(QIcon(self.main.app.storage.images.info.path))
        export_content.triggered.connect(self.get_export_content)
        self.main.tableView_exports.addAction(export_content)

        separator = QAction(self.main.tableView_imports)
        separator.setSeparator(True)
        self.main.tableView_exports.addAction(separator)

        load_answer = QAction(self.main.tableView_exports)
        load_answer.setText('Загрузить ответ')
        load_answer.setIcon(QIcon(self.main.app.storage.images.load.path))
        load_answer.triggered.connect(self.load_answer)
        self.main.tableView_exports.addAction(load_answer)

        open_import_protocol = QAction(self.main.tableView_exports)
        open_import_protocol.setText('Протокол импорта')
        open_import_protocol.setIcon(QIcon(self.main.app.storage.images.orders.path))
        open_import_protocol.triggered.connect(self.open_import_protocol)
        self.main.tableView_exports.addAction(open_import_protocol)

        open_init_protocol = QAction(self.main.tableView_exports)
        open_init_protocol.setText('Протокол идентификации')
        open_init_protocol.setIcon(QIcon(self.main.app.storage.images.orders.path))
        open_init_protocol.triggered.connect(self.open_init_protocol)
        self.main.tableView_exports.addAction(open_init_protocol)

    def open_import_protocol(self):
        export_item = self.selected_export()
        if export_item.model.answer_import:
            file = self.main.app.storage.answers.add_file('{}_import.xlsx'.format(export_item.model.id))
            if file.is_exists:
                file.start()
            else:
                QMessageBox.critical(self.main, 'Протокол', 'Файл {} отсутствует'.format(file.rel_path))
        else:
            QMessageBox.critical(self.main, 'Протокол', 'Ответ не загружался')

    def open_init_protocol(self):
        export_item = self.selected_export()
        if export_item.model.answer_import:
            file = self.main.app.storage.answers.add_file('{}_init.xlsx'.format(export_item.model.id))
            if file.is_exists:
                file.start()
            else:
                QMessageBox.critical(self.main, 'Протокол', 'Файл {} отсутствует'.format(file.rel_path))
        else:
            QMessageBox.critical(self.main, 'Протокол', 'Ответ не загружался')

    def get_table_content(self):
        table_model = ExportsTableModel(self.main.app)
        self.main.tableView_exports.setModel(table_model)
        self.main.tableView_exports.resizeColumnsToContents()

    def selected_export(self):
        export_id = self.main.tableView_exports.currentIndex().siblingAtColumn(1).data(Qt.DisplayRole)
        export_item = ExportData(self.main.app)
        export_item.get_export(export_id)
        return export_item

    def create_export_file(self):
        export_item = self.selected_export()
        try:
            export_item.create_export_file()
        except Exception as e:
            QMessageBox.warning(self.main, 'Файл выгрузки', 'Ошибка: {}'.format(e))

    def get_export_content(self):
        export_item = self.selected_export()
        message = []
        for index, row in enumerate(export_item.data()[:10]):
            message.append('{}. {} {} {} ({})'.format(index + 1, row[0], row[1], row[2], row[4]))
        QMessageBox.information(self.main, export_item.model.id, '\n'.join(message))

    def load_answer(self):
        export_item = self.selected_export()
        if export_item.model.answer_import:
            QMessageBox.information(self.main, 'Загрузка ответа', 'Для выгрузки {} ответ был загружен ранее'.format(export_item.model.id))
        else:
            self.main.tableView_exports.setEnabled(False)
            self.main.lineEdit_export_id.setText(export_item.model.id)
            self.main.respondent.set_fields_enabled()


class ExportsTableModel(QAbstractTableModel):

    def __init__(self, app):
        super(QAbstractTableModel, self).__init__()
        self.headers = ['number', 'id', 'created_utc', 'records_count', 'protocol', 'answer']
        self.description = ['№', 'Регистрационный номер', 'Дата/время', 'Количество', 'Протокол загрузки', 'Ответ СФР']
        self._data_ = ExportsListData(app).get_data()  # отображаемые записи в таблице

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
            if self._data_[index.row()][5] == 'OK':
                return QBrush(Qt.darkGreen)

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
