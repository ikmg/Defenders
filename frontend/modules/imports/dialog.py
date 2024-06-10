from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QMessageBox

from backend import DefendersApp
from frontend import Ui_Dialog_import
from .tv_data import ImportData
from tools import DTConvert
from .tv_dialog import DialogTableModel
from .import_item import ImportItem


class DialogImport(QDialog, Ui_Dialog_import):

    def __init__(self, app: DefendersApp, import_data: ImportData):
        self.app = app
        # self.import_item = import_data
        self.import_item = ImportItem(self, import_data)

        QDialog.__init__(self)
        self.setupUi(self)

        self.set_content()
        self.set_table_view()
        self.set_slots()
        self.set_buttons_enabled()

        self.show()

    def set_content(self):
        self.lineEdit_created_utc.setText(DTConvert(self.import_item.import_data.model.created_utc).dtstring)
        self.lineEdit_reg_num.setText(self.import_item.import_data.model.id)
        self.lineEdit_subject.setText(self.import_item.import_data.model.eskk_military_subject.short_name)
        self.lineEdit_contacts.setText(self.import_item.import_data.model.contact_info)
        self.lineEdit_stat.setText(str(self.import_item))
        self.lineEdit_status.setText('')

    def set_table_view(self):
        rows = self.import_item.import_data.dialog_table_model_rows()
        table_model = DialogTableModel(rows)
        self.tableView_rows.setSortingEnabled(True)
        self.tableView_rows.setModel(table_model)
        self.tableView_rows.horizontalHeader().resizeSection(0, 60)
        self.tableView_rows.horizontalHeader().resizeSection(1, 120)
        self.tableView_rows.horizontalHeader().resizeSection(2, 120)
        self.tableView_rows.horizontalHeader().resizeSection(3, 220)
        self.tableView_rows.horizontalHeader().resizeSection(4, 220)
        self.tableView_rows.horizontalHeader().resizeSection(5, 150)
        self.tableView_rows.horizontalHeader().resizeSection(6, 150)

    def set_slots(self):
        self.pushButton_received_file.setIcon(QIcon(self.app.storage.images.open.path))
        # self.pushButton_received_file.clicked.connect(self.open_received_file)
        self.pushButton_received_file.clicked.connect(self.import_item.open_received_file)

        self.pushButton_protocol_import.setIcon(QIcon(self.app.storage.images.import_p.path))
        # self.pushButton_protocol_import.clicked.connect(self.open_protocol_import)
        self.pushButton_protocol_import.clicked.connect(self.import_item.open_protocol_import)

        self.pushButton_protocol_init.setIcon(QIcon(self.app.storage.images.init_p.path))
        # self.pushButton_protocol_init.clicked.connect(self.open_protocol_init)
        self.pushButton_protocol_init.clicked.connect(self.import_item.open_protocol_init)

        self.pushButton_result_file.setIcon(QIcon(self.app.storage.images.result.path))
        # self.pushButton_result_file.clicked.connect(self.create_result_file)
        self.pushButton_result_file.clicked.connect(self.import_item.create_result_file)

        self.pushButton_import_finish.setIcon(QIcon(self.app.storage.images.finish.path))
        self.pushButton_import_finish.clicked.connect(self.finish_work)

        self.pushButton_import_delete.setIcon(QIcon(self.app.storage.images.delete.path))
        self.pushButton_import_delete.clicked.connect(self.delete_import)

        self.lineEdit_contacts.editingFinished.connect(self.edit_contacts)

    def set_buttons_enabled(self):
        if self.import_item.import_data.model.is_finished:
            self.pushButton_import_finish.setText('Отменить завершение работы')
            self.lineEdit_contacts.setEnabled(False)
            self.pushButton_import_delete.setEnabled(False)
        else:
            self.pushButton_import_finish.setText('Завершить работу')
            self.lineEdit_contacts.setEnabled(True)
            self.pushButton_import_delete.setEnabled(True)

        if not self.import_item.import_data.is_can_make_result:
            self.pushButton_import_finish.setEnabled(False)

        if not self.import_item.import_data.is_can_delete:
            self.pushButton_import_delete.setEnabled(False)

        if not self.import_item.import_data.is_can_make_result:
            self.pushButton_result_file.setEnabled(False)

    def edit_contacts(self):
        if self.lineEdit_contacts.text() != self.import_item.import_data.model.contact_info:
            msg = QMessageBox(self)
            msg.setWindowTitle('Изменение контакта')
            msg.setIcon(QMessageBox.Question)
            msg.setText('Контактные данные были изменены.\n\nСохранить изменения?'.format(
                self.import_item.import_data.model.id,
                self.import_item.import_data.model.eskk_military_subject.short_name))
            button_yes = msg.addButton("Сохранить!", QMessageBox.YesRole)
            button_no = msg.addButton("Нет, изменил случайно", QMessageBox.RejectRole)
            msg.setDefaultButton(button_no)

            msg.exec_()
            if msg.clickedButton() == button_yes:
                self.import_item.import_data.change_contacts(self.lineEdit_contacts.text())
            elif msg.clickedButton() == button_no:
                self.lineEdit_contacts.setText(self.import_item.import_data.model.contact_info)

    # def open_received_file(self):
    #     self.import_item.open_received_file()
        # try:
        #     self.import_item.import_data.original_file.start()
        # except Exception as e:
        #     QMessageBox.warning(self, 'Поступивший файл', 'Ошибка: {}'.format(e))

    # def open_protocol_import(self):
    #     self.import_item.open_protocol_import()
        # try:
        #     self.import_item.import_data.create_import_protocol()
        # except Exception as e:
        #     QMessageBox.warning(self, 'Протокол загрузки', 'Ошибка: {}'.format(e))

    # def open_protocol_init(self):
    #     self.import_item.open_protocol_init()
        # try:
        #     self.import_item.import_data.create_init_protocol()
        # except Exception as e:
        #     QMessageBox.warning(self, 'Протокол идентификации', 'Ошибка: {}'.format(e))

    # def create_result_file(self):
    #     self.import_item.create_result_file()
        # try:
        #     self.import_item.create_result_file()
        # except Exception as e:
        #     QMessageBox.critical(self, 'Результирующий файл', 'Ошибка: {}'.format(e))

    def finish_work(self):
        self.import_item.finish_work()
        self.set_buttons_enabled()

    def delete_import(self):
        if self.import_item.delete_import():
            self.close()
        # msg = QMessageBox(self)
        # msg.setWindowTitle('Удаление загрузки')
        # msg.setIcon(QMessageBox.Question)
        # msg.setText('Загрузка будет удалена.\n\nНомер: {}\nСубъект: {}\n\nВы уверены?'.format(
        #             self.import_item.import_data.model.id,
        #             self.import_item.import_data.model.eskk_military_subject.short_name))
        # button_yes = msg.addButton("Да я уверен!", QMessageBox.YesRole)
        # button_no = msg.addButton("Передумал", QMessageBox.RejectRole)
        # msg.setDefaultButton(button_no)
        #
        # msg.exec_()
        # if msg.clickedButton() == button_yes:
        #     try:
        #         self.import_item.delete_import()
        #         QMessageBox.information(self, 'Удаление загрузки', 'Загрузка {} успешно удалена'.format(self.import_item.import_data.model.id))
        #         self.close()
        #     except Exception as e:
        #         QMessageBox.critical(self, 'Удаление загрузки', 'Не удалось удалить загрузку {} ({})'.format(self.import_item.import_data.model.id, e))
