from database import Connection
from modules.loader.eskk import EskkLoader
from tools import work_directory, create_directory, get_new_path, csv_to_dict, is_path_exist
from tools.config import Config


class Root:
    """Базовый класс с корневым каталогом"""

    def __init__(self, root):
        self.root = root  # корневой каталог

    def subject_directory(self, subject_id):
        return create_directory(self.root, subject_id)


class Images(Root):
    """Изображения для интерфейса программы"""

    def __init__(self, root):
        super().__init__(root)
        self.icon = get_new_path(self.root, 'icon.ico')

        self.delete = get_new_path(self.root, 'delete.png')
        self.finish = get_new_path(self.root, 'finish.png')
        self.import_p = get_new_path(self.root, 'import_p.png')
        self.init_p = get_new_path(self.root, 'init_p.png')
        self.open = get_new_path(self.root, 'open.png')
        self.refresh = get_new_path(self.root, 'refresh.png')
        self.result = get_new_path(self.root, 'result.png')
        self.undo = get_new_path(self.root, 'undo.png')

        self.folder = get_new_path(self.root, 'folder.png')
        self.rosgvard = get_new_path(self.root, 'rg.png')


class Eskk(Root):
    """Справочники для базы данных и их содержание"""

    def __init__(self, root):
        super().__init__(root)
        self.genders = get_new_path(self.root, 'genders.csv')
        self.document_types = get_new_path(self.root, 'document_types.csv')
        self.military_ranks = get_new_path(self.root, 'military_ranks.csv')
        self.military_subjects = get_new_path(self.root, 'military_subjects.csv')

    def genders_data(self):
        return csv_to_dict(self.genders) if is_path_exist(self.genders) else []

    def document_types_data(self):
        return csv_to_dict(self.document_types) if is_path_exist(self.document_types) else []

    def military_ranks_data(self):
        return csv_to_dict(self.military_ranks) if is_path_exist(self.military_ranks) else []

    def military_subjects_data(self):
        return csv_to_dict(self.military_subjects) if is_path_exist(self.military_subjects) else []


class Storage(Root):
    """Хранилище файлов программы"""

    def __init__(self, root):
        super().__init__(root)
        self.images = Images(create_directory(self.root, 'images'))
        self.eskk = Eskk(create_directory(self.root, 'eskk'))
        self.defenders = Root(create_directory(self.root, 'defenders'))
        self.orders = Root(create_directory(self.root, 'orders'))
        self.exports = Root(create_directory(self.root, 'exports'))
        self.migration = Root(create_directory(self.root, 'migration'))
        self.answers = Root(create_directory(self.root, 'answers'))


class Application(Root):
    """Конфигурация приложения"""

    def __init__(self, root=work_directory()):
        super().__init__(root)
        self.settings = get_new_path(self.root, 'config.ini')  # путь к конфигу программы
        self.storage = Storage(create_directory(self.root, 'storage'))  # каталог хранилища файлов
        self.database = get_new_path(self.storage.root, 'defenders.db')  # путь к базе данных
        self.config = Config(self.settings, self.database)
        # DATABASE CONNECTION
        self.db_connection = Connection(self.config.db_uri, self.config.echo_mode)
        self.db_connection.create_db()
        self.update_handbooks()

    def update_handbooks(self):
        eskk = EskkLoader(self.db_connection.session)
        eskk.update_genders(self.storage.eskk.genders_data())
        eskk.update_document_types(self.storage.eskk.document_types_data())
        eskk.update_military_ranks(self.storage.eskk.military_ranks_data())
        eskk.update_military_subjects(self.storage.eskk.military_subjects_data())
