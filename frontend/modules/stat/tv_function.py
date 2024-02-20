from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from tools import DTConvert
from .imports import ImportSubjectsTableView, ImportCountTableView
from .participants import ParticipantsTableView, ParticipantsErrorsTableView


class StatTableViewer:

    def __init__(self, main):
        self.main = main
        self.main.tableView_statistic_data.setSortingEnabled(False)
        self.main.pushButton_save_statistic.setIcon(QIcon(self.main.app.storage.images.orders.path))
        self.main.pushButton_save_statistic.pressed.connect(self.download)
        # self.main.pushButton_save_statistic.pressed.connect(self.download)
        self.stat_types = {
            'import_count': {'index': 0, 'name': 'Загруженные файлы (количество)', 'table_view': ImportCountTableView},
            'import_subjects': {'index': 1, 'name': 'Загруженные файлы (по субъектам)', 'table_view': ImportSubjectsTableView},
            'participants_count': {'index': 2, 'name': 'Участники (по периодам)', 'table_view': ParticipantsTableView},
            'participants_errors': {'index': 3, 'name': 'Приказы (ошибки)', 'table_view': ParticipantsErrorsTableView}
            # 'export_files': {'index': 2, 'name': 'Выгруженные файлы', 'table_view': None},
            # 'defenders_count': {'index': 3, 'name': 'Защитники Отечества', 'table_view': None},

        }
        self.current_type = None
        self.table_model = None
        self.init_combo_box_content()
        self.main.comboBox_select_statistic.currentTextChanged.connect(self.get_table_content)

    def download(self):
        if self.current_type and self.table_model:
            file_name = '{}_{}.csv'.format(self.current_type, DTConvert().date)
            destination = self.main.app.storage.stat.add_file(file_name)
            self.table_model.download(destination.path)
            destination.start()

    def init_combo_box_content(self):
        for stat_type in self.stat_types:
            self.main.comboBox_select_statistic.addItem(self.stat_types[stat_type]['name'])
            self.main.comboBox_select_statistic.setItemData(self.stat_types[stat_type]['index'], stat_type, Qt.UserRole)
        self.main.comboBox_select_statistic.setEditable(False)
        self.main.comboBox_select_statistic.setCurrentIndex(0)
        self.get_table_content()

    def selected_stat(self):
        return self.main.comboBox_select_statistic.itemData(
            self.main.comboBox_select_statistic.currentIndex(),
            Qt.UserRole
        )

    def get_table_content(self):
        self.current_type = self.selected_stat()
        self.table_model = self.stat_types[self.current_type]['table_view'](self.main.app)
        self.main.tableView_statistic_data.setModel(self.table_model)
        self.main.tableView_statistic_data.resizeColumnsToContents()
