from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


class Menu:

    def __init__(self, main):
        self.main = main
        #
        self.main.action_exit.triggered.connect(self.main.close)
        #
        self.main.menu_catologs.setIcon(QIcon(self.main.app.storage.images.folder_open.path))

        self.main.action_storage_imports.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_imports.triggered.connect(self.main.app.storage.imports.open)

        self.main.action_storage_exports.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_exports.triggered.connect(self.main.app.storage.exports.open)

        self.main.action_storage_answers.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_answers.triggered.connect(self.main.app.storage.answers.open)

        self.main.action_storage_orders.setIcon(QIcon(self.main.app.storage.images.folder.path))
        self.main.action_storage_orders.triggered.connect(self.main.app.storage.orders.open)
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

    def clear_storage(self):
        QMessageBox.information(self.main, 'Новая функция', 'находится в разработке')

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
