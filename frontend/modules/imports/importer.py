from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from backend import ImportUploader
from database import EskkMilitarySubject
from tools import File


class Importer:

    def __init__(self, main):
        self.main = main
        self.import_workbook = None
        self.init_combo_box_content()
        self.main.comboBox_select_import_subject.currentTextChanged.connect(self.set_fields_enabled)
        self.main.pushButton_select_import_file.setIcon(QIcon(self.main.app.storage.images.folder_open.path))
        self.main.pushButton_select_import_file.pressed.connect(self.select_import_file_dialog)
        self.main.pushButton_load_import.setIcon(QIcon(self.main.app.storage.images.load.path))
        self.main.pushButton_load_import.pressed.connect(self.load_import)
        self.set_fields_enabled()

    def init_combo_box_content(self):
        subjects = []
        models = self.main.app.database.session.query(EskkMilitarySubject)
        models = models.order_by(EskkMilitarySubject.short_name)
        models = models.all()
        for model in models:
            if model.conditional_short_name:
                subjects.append([model.id, '{} ({})'.format(model.short_name, model.conditional_short_name)])
            else:
                subjects.append([model.id, '{}'.format(model.short_name)])
        for index, subject in enumerate(subjects):
            self.main.comboBox_select_import_subject.addItem(subject[1])
            self.main.comboBox_select_import_subject.setItemData(index, subject[0], Qt.UserRole)
        self.main.comboBox_select_import_subject.setEditable(True)
        self.main.comboBox_select_import_subject.setCurrentIndex(-1)

    def selected_subject_id(self):
        return self.main.comboBox_select_import_subject.itemData(
            self.main.comboBox_select_import_subject.currentIndex(),
            Qt.UserRole
        )

    def set_import_workbook(self, file_path):
        return ImportUploader(
            self.main.app.database.session,
            self.selected_subject_id(),
            file_path
        )

    def set_fields_enabled(self):
        self.main.label_import_workbook.setEnabled(False)
        self.main.pushButton_select_import_file.setEnabled(False)
        self.main.label_import_worksheet.setEnabled(False)
        self.main.comboBox_import_worksheet.setEnabled(False)
        self.main.pushButton_load_import.setEnabled(False)
        if self.selected_subject_id():
            self.main.pushButton_select_import_file.setEnabled(True)
            if self.main.lineEdit_import_filename.text():
                self.main.label_import_workbook.setEnabled(True)
                self.main.label_import_worksheet.setEnabled(True)
                self.main.comboBox_import_worksheet.setEnabled(True)
                if self.main.comboBox_import_worksheet.currentText():
                    self.main.pushButton_load_import.setEnabled(True)

    def select_import_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Загрузка файла", self.main.app.get_param('import_load_dir'), "Файлы (*.ods *.xls *.xlsx);;Все файлы (*)")
        file = File(file_path)
        if file.path:
            self.main.app.set_param('import_load_dir', file.dir.path)
            self.main.lineEdit_import_filename.setText(file.path)
            try:
                workbook = self.set_import_workbook(file.path)
                workbook.workbook.load()
                self.main.comboBox_import_worksheet.addItems(workbook.workbook.worksheets_list)
                self.set_fields_enabled()
            except Exception as e:
                self.main.lineEdit_import_filename.clear()
                QMessageBox.critical(self.main, 'Выбор файла', 'Ошибка: {}'.format(e))

    def load_import(self):
        if self.main.lineEdit_contacts.text():

            msg = QMessageBox(self.main)
            msg.setWindowTitle('Загрузка файла')
            msg.setIcon(QMessageBox.Question)
            msg.setText('Субъект: {}\nФайл: {}\nЛист: {}'.format(
                self.main.comboBox_select_import_subject.currentText(),
                self.main.lineEdit_import_filename.text(),
                self.main.comboBox_import_worksheet.currentText()
            ))
            button_yes = msg.addButton("Загрузить файл", QMessageBox.YesRole)
            button_no = msg.addButton("Передумал", QMessageBox.RejectRole)
            msg.setDefaultButton(button_no)
            msg.exec_()

            if msg.clickedButton() == button_yes:
                try:
                    workbook = self.set_import_workbook(self.main.lineEdit_import_filename.text())
                    directory = self.main.app.storage.imports.add_dir(workbook.subject_id)
                    destination = directory.add_file('{}{}'.format(workbook.import_id, workbook.workbook.file.extension))
                    workbook.workbook.load()
                    workbook.workbook.select_worksheet(self.main.comboBox_import_worksheet.currentText())
                    workbook.upload(destination.path, self.main.lineEdit_contacts.text())
                    self.main.lineEdit_contacts.clear()
                    # self.main.label_export_allow.setText(self.set_export_count())
                    QMessageBox.information(self.main, 'Загрузка файла', 'Файл успешно загружен')
                    self.main.imports_table_view.get_table_content()
                except Exception as e:
                    QMessageBox.critical(self.main, 'Загрузка файла', 'Ошибка: {}'.format(e))
            self.main.lineEdit_import_filename.clear()
            self.main.comboBox_import_worksheet.clear()
            self.set_fields_enabled()
        else:
            QMessageBox.warning(self.main, 'Импорт данных', 'Заполните контактные данные отправителя')
