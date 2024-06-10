from PyQt5.QtWidgets import QMessageBox

from .tv_data import ImportData


class ImportItem:

    def __init__(self, main, import_data: ImportData):
        self.main = main
        self.import_data = import_data

    def open_received_file(self):
        try:
            self.import_data.original_file.start()
        except Exception as e:
            QMessageBox.warning(self.main, 'Поступивший файл', 'Ошибка: {}'.format(e))

    def open_protocol_import(self):
        try:
            self.import_data.create_import_protocol()
        except Exception as e:
            QMessageBox.warning(self.main, 'Протокол загрузки', 'Ошибка: {}'.format(e))

    def open_protocol_init(self):
        try:
            self.import_data.create_init_protocol()
        except Exception as e:
            QMessageBox.warning(self.main, 'Протокол идентификации', 'Ошибка: {}'.format(e))

    def create_result_file(self):
        try:
            self.import_data.create_result_file()
        except Exception as e:
            QMessageBox.critical(self.main, 'Результирующий файл', 'Ошибка: {}'.format(e))

    def finish_work(self):
        self.import_data.finish_work()

    def delete_import(self) -> bool:
        msg = QMessageBox(self.main)
        msg.setWindowTitle('Удаление загрузки')
        msg.setIcon(QMessageBox.Question)
        msg.setText('Загрузка будет удалена.\n\nНомер: {}\nСубъект: {}\n\nВы уверены?'.format(
                    self.import_data.model.id,
                    self.import_data.model.eskk_military_subject.short_name))
        button_yes = msg.addButton("Да я уверен!", QMessageBox.YesRole)
        button_no = msg.addButton("Передумал", QMessageBox.RejectRole)
        msg.setDefaultButton(button_no)

        msg.exec_()
        if msg.clickedButton() == button_yes:
            try:
                self.import_data.delete_import()
                QMessageBox.information(self.main, 'Удаление загрузки', 'Загрузка {} успешно удалена'.format(self.import_data.model.id))
                return True
            except Exception as e:
                QMessageBox.critical(self.main, 'Удаление загрузки', 'Не удалось удалить загрузку {} ({})'.format(self.import_data.model.id, e))
                return False
