from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from backend import OrdersUploader
from tools import File


class Loader:

    def __init__(self, main):
        self.main = main
        self.loader = None

        self.main.pushButton_select_order_file.setIcon(QIcon(self.main.app.storage.images.folder_open.path))
        self.main.pushButton_select_order_file.pressed.connect(self.select_orders_file_dialog)

        self.main.pushButton_load_orders.setIcon(QIcon(self.main.app.storage.images.load.path))
        self.main.pushButton_load_orders.pressed.connect(self.load_orders)

        self.enable_orders_fields()

    def select_orders_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self.main,
            'Загрузка приказов',
            self.main.app.get_param('order_load_dir'),
            'Приказы ОШУ Росгвардии (*.xlsx)')
        file = File(filepath)
        if file.extension:
            try:
                self.main.app.set_param('order_load_dir', file.dir.path)
                self.main.lineEdit_order_filename.setText(file.path)
                self.loader = OrdersUploader(self.main.app.database.session, file.path)
                self.loader.workbook.load()
                self.main.lineEdit_order_filename.setText(file.path)
                self.enable_orders_fields()
            except Exception as e:
                QMessageBox.critical(self.main, 'Загрузка приказов', 'Ошибка: {}'.format(e))
        else:
            QMessageBox.critical(self.main, 'Загрузка приказов', 'Необходимо выбрать файл')

    def enable_orders_fields(self):
        self.main.pushButton_load_orders.setEnabled(False)
        if self.main.lineEdit_order_filename.text():
            self.main.pushButton_load_orders.setEnabled(True)

    def load_orders(self):
        try:
            destination = self.main.app.storage.orders.add_file(self.loader.storage_filename)
            self.loader.upload(destination.path)
            self.main.app.database.session.commit()
            self.main.lineEdit_order_filename.clear()
            self.enable_orders_fields()
        except Exception as e:
            QMessageBox.critical(self.main, 'Загрузка приказов', 'Ошибка: {}'.format(e))
