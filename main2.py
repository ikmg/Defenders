import sys

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QLockFile
from PyQt5.QtWidgets import QMainWindow, QSplashScreen, QApplication, QMessageBox

from backend import DefendersApp
from frontend import Ui_MainWindow, Menu  # интерфейс и меню
from frontend import StatTableViewer  # таб Статистика
from frontend import ImportsTableViewer, Importer  # таб Загрузки
from frontend import ExportsTableViewer, Exporter, Responder  # таб Выгрузки
from frontend import DefendersTableViewer  # таб Защитники
from frontend import ParticipantsTableViewer, Loader  # таб Участники
from tools import File

# надо
import pyexcel
import pyexcel_io
import pyexcel_ods
import pyexcel_xls
from pyexcel_io import writers


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.app = DefendersApp()
        # заставка
        pixmap = QPixmap("storage/images/loading.jpg")
        splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        splash.showMessage('<{}> загрузка...'.format(self.app.version), alignment=Qt.AlignBottom)
        splash.show()
        # погнали
        self.setupUi(self)
        self.setWindowIcon(QIcon(self.app.storage.images.icon.path))
        self.setWindowTitle('{} ({})'.format(self.windowTitle(), self.app.version))
        self.move(QApplication.desktop().availableGeometry().center() - self.rect().center())
        # оконное меню
        self.menu = Menu(self)
        # таб статистики
        self.tabWidget.setTabIcon(0, QIcon(self.app.storage.images.stat.path))
        self.stat = StatTableViewer(self)
        # таб с загрузками
        self.tabWidget.setTabIcon(1, QIcon(self.app.storage.images.imports.path))
        self.importer = Importer(self)
        self.imports_table_view = ImportsTableViewer(self)
        # таб с выгрузками
        self.tabWidget.setTabIcon(2, QIcon(self.app.storage.images.exports.path))
        self.exporter = Exporter(self)
        self.exports_table_view = ExportsTableViewer(self)
        self.respondent = Responder(self)
        # таб с защитниками
        self.tabWidget.setTabIcon(3, QIcon(self.app.storage.images.defenders.path))
        self.defenders = DefendersTableViewer(self)
        # таб с участниками
        self.tabWidget.setTabIcon(4, QIcon(self.app.storage.images.orders.path))
        self.participants = ParticipantsTableViewer(self)
        self.loader = Loader(self)
        # отображение главного окна
        splash.finish(self)
        self.show()


if __name__ == '__main__':
    lock_file = QLockFile(File(".lock").path)
    if not lock_file.tryLock():
        a = QApplication([])
        QMessageBox.critical(None, "Ошибка", "Приложение уже запущено!")
    else:
        app = QApplication(sys.argv)
        mw = MainWindow()
        sys.exit(app.exec_())
