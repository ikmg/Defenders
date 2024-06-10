from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from backend import AnswerUploader
from tools import File


class Responder:

    def __init__(self, main):
        self.main = main

        self.main.pushButton_answer_cancel.setIcon(QIcon(self.main.app.storage.images.delete.path))
        self.main.pushButton_answer_cancel.pressed.connect(self.cancel_answer)

        self.main.pushButton_select_answer_import.setIcon(QIcon(self.main.app.storage.images.folder_open.path))
        self.main.pushButton_select_answer_import.pressed.connect(self.select_answer_import_file_dialog)

        self.main.pushButton_select_answer_init.setIcon(QIcon(self.main.app.storage.images.folder_open.path))
        self.main.pushButton_select_answer_init.pressed.connect(self.select_answer_init_file_dialog)

        self.main.pushButton_load_answers.setIcon(QIcon(self.main.app.storage.images.load.path))
        # self.main.pushButton_load_answers.pressed.connect(self.load_answers)

        self.set_fields_enabled()

    def set_load_mode(self):
        self.main.pushButton_load_answers.pressed.connect(self.load_answers)

    def set_update_mode(self):
        self.main.pushButton_load_answers.pressed.connect(self.update_answers)

    def cancel_answer(self):
        self.main.lineEdit_export_id.clear()
        self.main.lineEdit_answer_import_filename.clear()
        self.main.lineEdit_answer_init_filename.clear()
        self.set_fields_enabled()
        self.main.tableView_exports.setEnabled(True)

    def select_answer_import_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self.main,
            'Протокол загрузки СФР',
            self.main.app.get_param('answer_load_dir'),
            'Протокол загрузки (*_import.xlsx)')
        file = File(filepath)
        if file.extension:
            self.main.app.set_param('answer_load_dir', file.dir.path)
            self.main.lineEdit_answer_import_filename.setText(file.path)
        self.set_fields_enabled()

    def select_answer_init_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self.main,
            'Протокол идентификации СФР',
            self.main.app.get_param('answer_load_dir'),
            'Протокол идентификации (*_init.xlsx)')
        file = File(filepath)
        if file.extension:
            self.main.app.set_param('answer_load_dir', file.dir.path)
            self.main.lineEdit_answer_init_filename.setText(file.path)
        self.set_fields_enabled()

    def set_fields_enabled(self):
        self.main.label_export_id.setEnabled(False)
        self.main.label_answer_import.setEnabled(False)
        self.main.label_answer_init.setEnabled(False)

        self.main.pushButton_answer_cancel.setEnabled(False)
        self.main.pushButton_select_answer_import.setEnabled(False)
        self.main.pushButton_select_answer_init.setEnabled(False)
        self.main.pushButton_load_answers.setEnabled(False)

        if self.main.lineEdit_export_id.text():
            self.main.label_export_id.setEnabled(True)
            self.main.label_answer_import.setEnabled(True)
            self.main.label_answer_init.setEnabled(True)

            self.main.pushButton_answer_cancel.setEnabled(True)
            self.main.pushButton_select_answer_import.setEnabled(True)
            self.main.pushButton_select_answer_init.setEnabled(True)

            if self.main.lineEdit_answer_import_filename.text() and self.main.lineEdit_answer_init_filename.text():
                self.main.pushButton_load_answers.setEnabled(True)

    def upload(self, is_update_mode: bool):
        export_item = self.main.exports_table_view.selected_export()
        import_file = File(self.main.lineEdit_answer_import_filename.text())
        init_file = File(self.main.lineEdit_answer_init_filename.text())
        if import_file.is_exists and init_file.is_exists:
            try:
                uploader = AnswerUploader(self.main.app.database.session, import_file.path, init_file.path)
                if not is_update_mode:
                    uploader.save(export_item.model.id)
                else:
                    uploader.update(export_item.model.id)

                import_file.copy(self.main.app.storage.answers.add_file('{}_import{}'.format(export_item.model.id, import_file.extension)).path)
                init_file.copy(self.main.app.storage.answers.add_file('{}_init{}'.format(export_item.model.id, init_file.extension)).path)
                self.main.app.database.session.commit()
                self.cancel_answer()
                QMessageBox.information(self.main, 'Загрузка ответа', 'Ответ для выгрузки {} успешно загружен'.format(export_item.model.id))
                self.main.exports_table_view.get_table_content()
            except Exception as e:
                self.main.app.database.session.rollback()
                self.cancel_answer()
                QMessageBox.critical(self.main, 'Загрузка ответа', 'Ошибки:{}'.format(e))

    def load_answers(self):
        self.upload(is_update_mode=False)

    def update_answers(self):
        self.upload(is_update_mode=True)
