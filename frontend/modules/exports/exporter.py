from PyQt5.QtWidgets import QMessageBox

from backend import ProvidedReportHandler, export_data
from frontend.modules.exports.tv_data import ExportData


class Exporter:

    def __init__(self, main):
        self.main = main
        self.main.pushButton_export_data.pressed.connect(self.make_export)

    def make_export(self):
        provider = ProvidedReportHandler(self.main.app.database.session)
        if provider.count > 0:
            msg = QMessageBox(self.main)
            msg.setWindowTitle('Создание выгрузки')
            msg.setIcon(QMessageBox.Question)
            msg.setText('Для выгрузки доступно {} записей. Желаете продолжить?'.format(provider.count))
            button_yes = msg.addButton("Создать выгрузку", QMessageBox.YesRole)
            button_no = msg.addButton("Передумал", QMessageBox.RejectRole)
            msg.setDefaultButton(button_no)
            msg.exec_()
            if msg.clickedButton() == button_yes:
                model = provider.make_export()

                export_data = ExportData(self.main.app)
                export_data.get_export(model.id)
                export_data.create_export_file()

                self.main.exports_table_view.get_table_content()
                self.main.imports_table_view.get_table_content()
                QMessageBox.information(self.main, 'Создание выгрузки', 'Выгружено {} записей'.format(provider.count))
        else:
            QMessageBox.information(self.main, 'Создание выгрузки', 'Прежде чем что-то выгрузить нужно что-то загрузить без критических ошибок')
