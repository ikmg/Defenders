from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from tools import DTConvert
from .imports import ImportSubjectsTableView, ImportCountTableView
from .participants import ParticipantsTableView, ParticipantsErrorsTableView


class StatTableViewer:

    def __init__(self, main):
        self.main = main
        self.main.tableView_statistic_data.setSortingEnabled(False)

        self.tmp_order = [
            'import_count',
            'import_subjects',
            'participants_count',
            'participants_errors'
        ]

        self.stat_types = {
            'import_count': {'index': 0, 'name': 'Загруженные файлы (сводные сведения)', 'table_view': ImportCountTableView},
            'import_subjects': {'index': 1, 'name': 'Загруженные файлы (по субъектам)', 'table_view': ImportSubjectsTableView},
            'participants_count': {'index': 2, 'name': 'Приказы (по участникам и периодам)', 'table_view': ParticipantsTableView},
            'participants_errors': {'index': 3, 'name': 'Приказы (не загруженные строки файла)', 'table_view': ParticipantsErrorsTableView}
            # 'export_files': {'index': 2, 'name': 'Выгруженные файлы', 'table_view': None},
            # 'defenders_count': {'index': 3, 'name': 'Защитники Отечества', 'table_view': None},

        }
        self.current_type = None
        self.table_model = None
        self.init_combo_box_content()

        self.main.comboBox_select_statistic.currentTextChanged.connect(self.get_table_content)

        self.main.pushButton_refresh_statistic.setIcon(QIcon(self.main.app.storage.images.refresh.path))
        self.main.pushButton_refresh_statistic.pressed.connect(self.get_table_content)

        self.main.pushButton_save_statistic.setIcon(QIcon(self.main.app.storage.images.orders.path))
        self.main.pushButton_save_statistic.pressed.connect(self.download)

    def download(self):
        if self.current_type and self.table_model:
            file_name = '{}_{}.csv'.format(self.current_type, DTConvert().date)
            destination = self.main.app.storage.stat.add_file(file_name)
            self.table_model.download(destination.path)
            destination.start()

    def init_combo_box_content(self):
        for stat_type in self.tmp_order:
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
        # print('подсчет статистики {}'.format(self.current_type))
        self.table_model = self.stat_types[self.current_type]['table_view'](self.main.app)
        self.main.tableView_statistic_data.setModel(self.table_model)
        if self.current_type == 'participants_errors':
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(0, 60)
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(1, 300)
        elif self.current_type == 'participants_count':
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(0, 150)
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(1, 150)
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(2, 100)
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(3, 150)
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(4, 150)
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(5, 150)
            self.main.tableView_statistic_data.horizontalHeader().resizeSection(6, 150)
        else:
            self.main.tableView_statistic_data.resizeColumnsToContents()
