import os
import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QLockFile, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QFileDialog, QHeaderView, QAction, QSplashScreen

from database import KeepedReport, KeepedReportRecord
from backend.interface import ImportUI
from frontend.interface.main_window import Ui_MainWindow
from frontend.interface.utils.combo_box import subjects_combo_box_items
from frontend.interface.utils.table_view import ImportsTableView, ParticipantsTableView, DefendersTableView, ExportTableView, StatImportsTableView
from backend.upload.handler import KeepedReportHandler, KeepedOrderHandler
from backend.upload.handler.provider import ProvidedReportHandler
from backend.upload.handler.answer import AnswerChecker
from backend.download.exporter import sfr_export_data
from backend import DefendersApp
from backend.download.csv import write_csv_list
from tools import File
from backend.download.wokbooks.xls_file import report_result


class MainWindow(QMainWindow, Ui_MainWindow):
    """

    """
    def __init__(self):
        pixmap = QPixmap("storage/images/loading.jpg")
        splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)

        splash.showMessage('Загрузка...', alignment=Qt.AlignBottom)
        splash.show()

        QMainWindow.__init__(self)
        splash.showMessage('Проверка целостности...', alignment=Qt.AlignBottom)
        self.app = DefendersApp()
        splash.showMessage('<{}> Подготовка интерфейса...'.format(self.app.version), alignment=Qt.AlignBottom)

        self.setupUi(self)
        QMainWindow.setWindowTitle(self, '{} ({})'.format(QMainWindow.windowTitle(self), self.app.version))

        desc = QApplication.desktop()
        self.setWindowIcon(QIcon(self.app.storage.images.icon.path))
        self.move(desc.availableGeometry().center() - self.rect().center())

        # GLOBALS
        self.import_subject_id = None
        self.import_object = None
        self.export_object = None
        self.user_search = False

        # ----
        # TABS
        # ----

        # STATIC TAB
        # data
        self.set_table_view_stat_imports_model()

        # IMPORT TAB
        # interface
        self.tableView_imports.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.init_menu_imports()
        # data
        self.set_table_view_imports_model()
        self.init_combo_box_content()
        # buttons
        self.pushButton_select_import_file.pressed.connect(self.select_import_file_dialog)
        self.pushButton_load_import.pressed.connect(self.load_import)
        self.comboBox_select_import_subject.currentTextChanged.connect(self.enable_import_fields)

        # EXPORT TAB
        # interface
        self.tableView_exports.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.init_menu_exports()
        self.set_export_count()
        # data
        self.set_table_view_export_model()
        # buttons
        self.pushButton_export_data.pressed.connect(self.export_to_sfr)
        self.pushButton_select_answer_import.pressed.connect(self.select_answer_import_file_dialog)
        self.pushButton_select_answer_init.pressed.connect(self.select_answer_init_file_dialog)
        self.pushButton_load_answers.pressed.connect(self.load_answers)

        # DEFENDER TAB
        self.lineEdit_find_defender.setText('Текст для поиска')
        self.lineEdit_find_defender.returnPressed.connect(self.find_table_view_defenders_model)
        self.set_table_view_defenders_model()

        # ORDER TAB
        self.pushButton_select_order_file.pressed.connect(self.select_orders_file_dialog)
        self.pushButton_load_orders.pressed.connect(self.load_orders)
        self.lineEdit_find_order_person.setText('Текст для поиска')
        self.lineEdit_find_order_person.returnPressed.connect(self.find_table_view_orders_model)
        self.set_table_view_orders_model()

        # EQUAL TAB
        # interface
        self.splitter_compare.setStretchFactor(1, 3)

        # ----
        # APP START
        # ----

        self.enable_import_fields()
        self.enable_orders_fields()
        # self.set_export_count()
        splash.finish(self)
        self.show()

    def selected_import_item(self):
        """
        Создает объект класса ImportUI из ячейки с индексом 2 выбранной строки
        :return: ImportUI
        """
        import_id = self.tableView_imports.currentIndex().siblingAtColumn(2).data(Qt.DisplayRole)
        import_item = ImportUI(self.app)
        import_item.get_model(import_id)
        return import_item

    # STATIC TAB METHODS

    def set_table_view_stat_imports_model(self):
        self.tableView_statistic_data.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_statistic_data.setModel(StatImportsTableView(self.app.database.session))

    # IMPORT TAB METHODS

    def init_combo_box_content(self):
        for index, subject in enumerate(subjects_combo_box_items(self.app.database.session)):
            self.comboBox_select_import_subject.addItem(subject[1])
            self.comboBox_select_import_subject.setItemData(index, subject[0], Qt.UserRole)
        self.comboBox_select_import_subject.setEditable(True)
        self.comboBox_select_import_subject.setCurrentIndex(-1)

    def init_menu_imports(self):
        self.tableView_imports.setContextMenuPolicy(Qt.ActionsContextMenu)

        received_file = QAction(self.tableView_imports)
        received_file.setText('Поступивший файл')
        received_file.setIcon(QIcon(self.app.storage.images.open.path))
        received_file.triggered.connect(self.get_received_file)

        protocol_import = QAction(self.tableView_imports)
        protocol_import.setText('Протокол импорта')
        protocol_import.setIcon(QIcon(self.app.storage.images.import_p.path))
        protocol_import.triggered.connect(self.get_protocol_import)

        protocol_identify = QAction(self.tableView_imports)
        protocol_identify.setText('Протокол идентификации')
        protocol_identify.setIcon(QIcon(self.app.storage.images.init_p.path))
        protocol_identify.triggered.connect(self.get_protocol_init)

        separator = QAction(self.tableView_imports)
        separator.setSeparator(True)

        finish_import = QAction(self.tableView_imports)
        finish_import.setText('Результирующий файл')
        finish_import.setIcon(QIcon(self.app.storage.images.result.path))
        finish_import.triggered.connect(self.set_import_finished)

        import_finished = QAction(self.tableView_imports)
        import_finished.setText('Завершить')
        import_finished.setIcon(QIcon(self.app.storage.images.finish.path))
        import_finished.triggered.connect(self.finish_import)

        delete_file = QAction(self.tableView_imports)
        delete_file.setText('Удалить')
        delete_file.setIcon(QIcon(self.app.storage.images.delete.path))
        delete_file.triggered.connect(self.delete_load)

        self.tableView_imports.addAction(received_file)
        self.tableView_imports.addAction(protocol_import)
        self.tableView_imports.addAction(protocol_identify)
        self.tableView_imports.addAction(separator)
        self.tableView_imports.addAction(finish_import)
        self.tableView_imports.addAction(import_finished)
        self.tableView_imports.addAction(delete_file)

    def set_table_view_imports_model(self):
        view = ImportsTableView(self.app)
        self.tableView_imports.setModel(view)

    def select_import_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Загрузка файла", self.app.get_param('import_load_dir'), "Файлы (*.ods *.xls *.xlsx);;Все файлы (*)")
        file = File(file_path)
        self.app.set_param('import_load_dir', file.dir)
        if file.path:
            self.lineEdit_import_filename.setText(file.path)
            self.import_object = KeepedReportHandler(self.app.database.session, **self.get_import_data())
            if self.import_object.is_model_exists:
                QMessageBox.warning(None, 'Открытие файла импорта', self.import_object.critical)
                self.lineEdit_import_filename.clear()
                self.comboBox_import_worksheet.clear()
                self.import_object = None
            else:
                self.comboBox_import_worksheet.addItems(self.import_object.workbook.worksheets_list)
        self.enable_import_fields()

    def load_import(self):
        if self.lineEdit_contacts.text():
            if self.import_object.model:
                self.import_object = KeepedReportHandler(self.app.database.session, **self.get_import_data())
                self.import_object.parsing()
                self.set_table_view_imports_model()
                QMessageBox.information(None, 'Импорт данных', 'Файл успешно загружен')
            else:
                QMessageBox.warning(None, 'Импорт данных', self.import_object.critical)
            self.app.database.session.commit()
            self.lineEdit_import_filename.clear()
            self.comboBox_import_worksheet.clear()
            self.lineEdit_contacts.clear()
            self.import_object = None
            self.enable_import_fields()
            self.label_export_allow.setText(self.set_export_count())
        else:
            QMessageBox.warning(None, 'Импорт данных', 'Заполните контактные данные отправителя')

    def enable_import_fields(self):
        self.import_subject_id = self.comboBox_select_import_subject.itemData(self.comboBox_select_import_subject.currentIndex(), Qt.UserRole)
        self.pushButton_select_import_file.setEnabled(False)
        self.comboBox_import_worksheet.setEnabled(False)
        self.lineEdit_contacts.setEnabled(False)
        self.pushButton_load_import.setEnabled(False)
        if self.import_subject_id:
            self.pushButton_select_import_file.setEnabled(True)
            if self.lineEdit_import_filename.text():
                self.comboBox_import_worksheet.setEnabled(True)
                if self.comboBox_import_worksheet.currentText():
                    self.lineEdit_contacts.setEnabled(True)
                    self.pushButton_load_import.setEnabled(True)

    def get_import_data(self):
        return {
            'contact_info': self.lineEdit_contacts.text(),
            'workbook': {
                'file_path': self.lineEdit_import_filename.text(),
                'subject_id': self.import_subject_id,
                'destination': self.app.storage.imports.subject_directory(self.import_subject_id),
                'debug_mode': self.app.settings.debug_mode
            }
        }

    def delete_load(self):
        import_item = self.selected_import_item()
        if import_item.model and import_item.is_can_delete:
            user_choice = QMessageBox.question(None, 'Удаление загрузки', 'Можно удалить файл. Вы уверены?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if user_choice == QMessageBox.Yes:
                if import_item.delete_import():
                    self.set_table_view_imports_model()
                    QMessageBox.information(None, 'Удаление загрузки', 'Загрузка {} успешно удалена'.format(import_item.model.id))
                else:
                    QMessageBox.critical(None, 'Удаление загрузки', 'Не удалось удалить загрузку {}'.format(import_item.model.id))
        else:
            QMessageBox.critical(None, 'Удаление загрузки', 'Невозможно удалить загрузку')

    def get_received_file(self):
        self.selected_import_item().open_original_file()

    def get_protocol_import(self):
        self.selected_import_item().create_import_protocol()

    def get_protocol_init(self):
        self.selected_import_item().create_init_protocol()

    def set_import_finished(self):
        import_item = self.selected_import_item()
        if import_item.is_can_make_result:
            try:
                q=1
                import_item.original_file_name.copy(import_item.result_file_name.path)
                # copy_file(convert_path(import_item.original_file_name), convert_path(import_item.result_file_name))
                result_data = []
                model = self.app.database.session.query(KeepedReport).join(KeepedReportRecord).filter(KeepedReport.id == import_item.model.id).order_by(KeepedReportRecord.file_row_num).scalar()
                for record in model.keeped_report_records:
                    if not record.is_find_in_orders:
                        # result_data.append('строка {}: Отсутствует в приказах ОШУ Росгвардии'.format(record.file_row_num))
                        result_data.append('ОШИБКА: отсутствует в приказах ОШУ Росгвардии')
                    elif record.critical_messages:
                        # result_data.append('строка {}: {}'.format(record.file_row_num, record.critical_messages))
                        result_data.append('КРИТИЧЕСКИЕ ОШИБКИ: {}'.format(record.critical_messages))
                    elif not record.provided_report_record.answer_init:
                        # result_data.append('строка {}: Ответ СФР России не поступал'.format(record.file_row_num))
                        result_data.append('Ответ СФР: не поступал')
                    else:
                        result_data.append('Ответ СФР: {}'.format(record.provided_report_record.answer_init.comment))
                report_result(import_item.result_file_name, result_data)
                import_item.open_result_file()
            except Exception as e:
                QMessageBox.critical(None, 'Результирующий файл', 'Ошибка: {}'.format(e.args))
        else:
            QMessageBox.warning(None, 'Результирующий файл', 'Невозможно создать результирующий файл')

    def finish_import(self):
        import_item = self.selected_import_item()
        if import_item.is_can_make_result:
            import_item.finish_work()
            self.set_table_view_imports_model()
        else:
            QMessageBox.critical(None, 'Завершение работы с файлом', 'Невозможно завершить работу')

    # EXPORT TAB METHODS

    def init_menu_exports(self):
        self.tableView_exports.setContextMenuPolicy(Qt.ActionsContextMenu)

        export_sfr_file = QAction(self.tableView_exports)
        export_sfr_file.setText('Открыть файл для отправки')
        export_sfr_file.triggered.connect(self.get_export_sfr_file)
        self.tableView_exports.addAction(export_sfr_file)

        export_sfr_fio = QAction(self.tableView_exports)
        export_sfr_fio.setText('Показать первые 10 фамилий')
        export_sfr_fio.triggered.connect(self.get_export_sfr_fio)
        self.tableView_exports.addAction(export_sfr_fio)

    def set_table_view_export_model(self):
        self.tableView_exports.setModel(ExportTableView(self.app.database.session))

    def set_export_count(self):
        self.export_object = ProvidedReportHandler(self.app.database.session)
        self.label_export_allow.setText('Доступно для выгрузки {} записей'.format(self.export_object.count))

    def export_to_sfr(self):
        if self.export_object.count > 0:
            self.export_object.export()
            self.set_table_view_export_model()
            QMessageBox.information(None, 'Экспорт данных', 'Успешно завершен')
        else:
            QMessageBox.warning(None, 'Экспорт данных', 'Отсутствуют данные для экспорта')
        self.set_export_count()
        self.set_table_view_imports_model()

    def select_answer_import_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(None, "Протокол загрузки СФР", self.app.get_param('answer_load_dir'), "Протокол загрузки (*_import.xlsx);;Все файлы (*)")
        self.app.set_param('answer_load_dir', get_path_from_file_path(filepath))
        if filepath:
            self.lineEdit_answer_import_filename.setText(filepath)

    def select_answer_init_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(None, "Протокол идентификации СФР", self.app.get_param('answer_load_dir'), "Протокол идентификации (*_init.xlsx);;Все файлы (*)")
        self.app.set_param('answer_load_dir', get_path_from_file_path(filepath))
        if filepath:
            self.lineEdit_answer_init_filename.setText(filepath)

    def load_answers(self):
        if self.lineEdit_answer_import_filename.text() and self.lineEdit_answer_init_filename.text():
            id = self.tableView_exports.currentIndex().siblingAtColumn(1).data(Qt.DisplayRole)
            ans = AnswerChecker(
                self.app.database.session,
                id,
                self.lineEdit_answer_import_filename.text(),
                self.lineEdit_answer_init_filename.text()
            )
            if ans.answer['is_ok']:
                ans.save()
                self.app.database.session.commit()
                QMessageBox.information(None, 'Ответ СФР', ans.result)
            #     TODO копировать файлы
                copy_file(
                    self.lineEdit_answer_import_filename.text(),
                    get_new_path(self.app.storage.answers.root, '{}_import.xlsx'.format(id))
                )
                copy_file(
                    self.lineEdit_answer_init_filename.text(),
                    get_new_path(self.app.storage.answers.root, '{}_init.xlsx'.format(id))
                )
                self.set_table_view_export_model()
            else:
                QMessageBox.warning(None, 'Ответ СФР', ans.result)
        self.lineEdit_answer_import_filename.setText('')
        self.lineEdit_answer_init_filename.setText('')
        self.set_table_view_imports_model()

    def get_export_sfr_file(self):
        export_id = self.tableView_exports.currentIndex().siblingAtColumn(1).data(Qt.DisplayRole)
        filename = self.app.storage.exports.root
        filename = get_new_path(filename, '{}.csv'.format(export_id))
        write_csv_list(filename, sfr_export_data(self.app.database.session, export_id))
        start_file(filename)

    def get_export_sfr_fio(self):
        export_id = self.tableView_exports.currentIndex().siblingAtColumn(1).data(Qt.DisplayRole)
        data = sfr_export_data(self.app.database.session, export_id)
        message = []
        for row in data[:10]:
            message.append('{} {} {} ({})'.format(row[0], row[1], row[2], row[4]))
        QMessageBox.information(None, export_id, '\n'.join(message))

    # DEFENDER TAB METHODS

    def find_table_view_defenders_model(self):
        self.user_search = True
        self.set_table_view_defenders_model()

    def set_table_view_defenders_model(self):
        self.tableView_defenders.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_defenders.setModel(DefendersTableView(self.app.database.session, self.lineEdit_find_defender.text(), self.user_search))

    # ORDER TAB METHODS

    def select_orders_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(None, "Загрузка файла", self.app.get_param('order_load_dir'), "Приказы ОШУ Росгвардии (*.ods *.xls *.xlsx);;Все файлы (*)")
        self.app.set_param('order_load_dir', get_path_from_file_path(filepath))
        if filepath:
            self.lineEdit_order_filename.setText(filepath)
            self.import_object = KeepedOrderHandler(self.app.database.session, **self.get_orders_data())
            if self.import_object.is_already_exists:
                QMessageBox.warning(None, 'Открытие файла импорта', self.import_object.critical)
                self.lineEdit_order_filename.clear()
                self.import_object = None
        self.enable_orders_fields()

    def load_orders(self):
        if self.import_object.model:
            # self.import_object = KeepedOrderHandler(self.app.database.session, **self.get_orders_data())
            self.import_object.clear_orders()
            self.import_object.parsing()
            self.set_table_view_orders_model()
            QMessageBox.information(None, 'Импорт данных', 'Файл успешно загружен')
        else:
            QMessageBox.warning(None, 'Импорт данных', self.import_object.critical)
        self.app.database.session.commit()
        self.lineEdit_order_filename.clear()
        self.import_object = None
        self.enable_orders_fields()

    def find_table_view_orders_model(self):
        self.user_search = True
        self.set_table_view_orders_model()

    def set_table_view_orders_model(self):
        self.tableView_order_persons.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_order_persons.setModel(ParticipantsTableView(self.app.database.session, self.lineEdit_find_order_person.text(), self.user_search))

    def enable_orders_fields(self):
        self.pushButton_load_orders.setEnabled(False)
        if self.lineEdit_order_filename.text():
            self.pushButton_load_orders.setEnabled(True)

    def get_orders_data(self):
        return {
            'file_path': self.lineEdit_order_filename.text(),
            'destination': self.app.storage.orders.root,
            'debug_mode': self.app.config.debug_mode
        }

    # EQUAL TAB METHODS


if __name__ == '__main__':
    lock_file = QLockFile(os.path.abspath(".lock"))
    if not lock_file.tryLock():
        a = QApplication([])
        QMessageBox.warning(None, "Ошибка повторного запуска", "Приложение уже запущено!")
    else:
        app = QApplication(sys.argv)
        # pixmap = QPixmap("storage/images/loading.gif")
        # splash = QSplashScreen(pixmap)
        # splash.show()
        # splash.showMessage('Загрузка...')
        mw = MainWindow()
        # splash.finish(mw)
        sys.exit(app.exec_())



