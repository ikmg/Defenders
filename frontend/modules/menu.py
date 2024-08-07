import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from backend import StorageInspector, get_sfr_control_rows, create_sfr_control_file
from backend.download.data.sfr_control import get_sfr_forgiven_rows
from backend.download.workbooks import create_sfr_forgiven_file
from tools import File


class Menu:

    def __init__(self, main):
        self.main = main
        #
        self.main.action_exit.triggered.connect(self.main.close)

        self.main.action_sfr_control.setIcon(QIcon(self.main.app.storage.images.exports.path))
        self.main.action_sfr_control.triggered.connect(self.sfr_control)

        self.main.action_forgiven_defenders.setIcon(QIcon(self.main.app.storage.images.search.path))
        self.main.action_forgiven_defenders.triggered.connect(self.sfr_forgiven)

        #
        self.main.menu_catalogs.setIcon(QIcon(self.main.app.storage.images.folder_open.path))

        self.main.action_storage_imports.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_imports.triggered.connect(self.main.app.storage.imports.open)

        self.main.action_storage_exports.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_exports.triggered.connect(self.main.app.storage.exports.open)

        self.main.action_storage_answers.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_answers.triggered.connect(self.main.app.storage.answers.open)

        self.main.action_storage_orders.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_orders.triggered.connect(self.main.app.storage.orders.open)

        self.main.action_storage_stat.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_stat.triggered.connect(self.main.app.storage.stat.open)

        self.main.action_storage.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage.triggered.connect(self.main.app.storage.root.open)
        #
        self.main.menu_eskk.setIcon(QIcon(self.main.app.storage.images.refresh.path))

        self.main.action_eskk_genders.setIcon(QIcon(self.main.app.storage.images.orders.path))
        self.main.action_eskk_genders.triggered.connect(self.update_eskk_genders)

        self.main.action_eskk_doc_types.setIcon(QIcon(self.main.app.storage.images.orders.path))
        self.main.action_eskk_doc_types.triggered.connect(self.update_eskk_doc_types)

        self.main.action_eskk_ranks.setIcon(QIcon(self.main.app.storage.images.orders.path))
        self.main.action_eskk_ranks.triggered.connect(self.update_eskk_ranks)

        self.main.action_eskk_subjects.setIcon(QIcon(self.main.app.storage.images.orders.path))
        self.main.action_eskk_subjects.triggered.connect(self.update_eskk_subjects)

        self.main.action_eskk_all.setIcon(QIcon(self.main.app.storage.images.orders.path))
        self.main.action_eskk_all.triggered.connect(self.update_eskk)

        self.main.action_clear_storage.setIcon(QIcon(self.main.app.storage.images.clear.path))
        self.main.action_clear_storage.triggered.connect(self.clear_storage)

        self.main.action_vacuum_db.setIcon(QIcon(self.main.app.storage.images.result.path))
        self.main.action_vacuum_db.triggered.connect(self.vacuum_db)

    def sfr_control(self):
        header = [
            '№',
            'Фамилия',
            'Имя',
            'Отчество',
            'Пол',
            'Дата рождения',
            'СНИЛС',
            'Тип',
            'Серия',
            'Номер',
            'Выдан',
            'Дата выгрузки',
            'Номер выгрузки, строка',
            'Ответ СФР'
        ]
        rows = get_sfr_control_rows(self.main.app.database.session)
        destination = self.main.app.storage.stat.add_file('sfr_control.xlsx')
        create_sfr_control_file(header, rows, destination.path)
        destination.start()

    def sfr_forgiven(self):
        header = [
            '№',
            'Фамилия',
            'Имя',
            'Отчество',
            'Пол',
            'Дата рождения',
            'СНИЛС',
            'Тип',
            'Серия',
            'Номер',
            'Выдан',
            'Дата выгрузки',
            'Номер выгрузки, строка',
            'Ответ СФР'
        ]
        rows = get_sfr_forgiven_rows(self.main.app.database.session)
        destination = self.main.app.storage.stat.add_file('sfr_forgiven.xlsx')
        create_sfr_forgiven_file(header, rows, destination.path)
        destination.start()

    def clear_storage(self):
        file_name = 'storage_inspector.txt'
        with open(file_name, 'w') as sys.stdout:
            inspector = StorageInspector(self.main.app)
            inspector.compare()
            res = inspector.clear()
        sys.stdout = sys.__stdout__
        QMessageBox.information(self.main, 'Зачистка хранилища', res)
        file = File(file_name)
        file.start()

    def vacuum_db(self):
        self.main.app.database.vacuum()
        QMessageBox.information(
            self.main,
            'Сжатие базы данных',
            'Завершено, текущий размер {} MB'.format(self.main.app.database.file.size_mb)
        )

    def update_eskk_genders(self):
        try:
            self.main.app.eskk_update_genders()
            self.done_message()
        except Exception as e:
            self.error_message(e)

    def update_eskk_doc_types(self):
        try:
            self.main.app.eskk_update_document_types()
            self.done_message()
        except Exception as e:
            self.error_message(e)

    def update_eskk_ranks(self):
        try:
            self.main.app.eskk_update_military_ranks()
            self.done_message()
        except Exception as e:
            self.error_message(e)

    def update_eskk_subjects(self):
        try:
            self.main.app.eskk_update_military_subjects()
            self.done_message()
        except Exception as e:
            self.error_message(e)

    def update_eskk(self):
        try:
            self.main.app.eskk_update_all()
            self.done_message()
        except Exception as e:
            self.error_message(e)

    def done_message(self):
        QMessageBox.information(self.main, 'Обновление', 'Успешно обновлено')

    def error_message(self, exception):
        QMessageBox.warning(self.main, 'Обновление справочников', 'Ошибка: {}'.format(exception))
