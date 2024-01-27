import datetime
from .fs import Directory, File, work_directory

from database import Connection, DefenderParameter
from modules.loader.eskk import EskkLoader
from .ini_files import ini_to_dict
from .csv_files import csv_to_dict


APP_VERSION = '3.0'
APP_RELEASE = '26.01.2024'


class Root:
    """
    Класс объекта приложения, который представляет собой директорию
    """

    def __init__(self, root_dir: Directory):
        """
        :param root_dir: Directory()
        """
        self.root = root_dir

    def __repr__(self):
        return self.root.path


class DefendersApp(Root):
    """
    Класс свойств приложения
    """

    def __init__(self, root_dir: Directory = work_directory()):
        """
        :param root_dir: Directory()
        """
        super().__init__(root_dir)
        self.log = []
        self.settings = Settings(self.root.add_file('config.ini'))
        self.storage = Storage(self.root.add_dir('storage'))
        self.database = Database(
            self.settings.db_dialect,
            self.storage.root.add_file('defenders.db').path,
            self.settings.echo_mode
        )
        self.set_param('version', APP_VERSION)
        self.set_param('release', APP_RELEASE)

    def update_handbooks(self):
        eskk = EskkLoader(self.database.session)
        eskk.update_genders(self.storage.eskk.genders_data())
        eskk.update_document_types(self.storage.eskk.document_types_data())
        eskk.update_military_ranks(self.storage.eskk.military_ranks_data())
        eskk.update_military_subjects(self.storage.eskk.military_subjects_data())

    def create_param(self, name: str, value: str):
        param = DefenderParameter()
        param.param = name
        param.value = value
        self.database.session.add(param)
        self.database.session.commit()

    def set_param(self, name: str, value: str):
        model = self.database.session.query(DefenderParameter).filter(DefenderParameter.param == name).scalar()
        if model:
            model.value = value
            self.database.session.commit()
        else:
            self.create_param(name, value)

    def get_param(self, name: str):
        model = self.database.session.query(DefenderParameter).filter(DefenderParameter.param == name).scalar()
        if model:
            return model.value
        else:
            self.create_param(name, '')
            return ''

    def print_log(self, text: str):
        log_row = [str(datetime.datetime.now()), text]
        self.log.append(log_row)
        if self.settings.debug_mode:
            print(' '.join(log_row))

    @property
    def version(self):
        return 'v.{} от {}'.format(
            self.get_param('version'),
            self.get_param('release')
        )


class Settings:

    def __init__(self, config_file: File):
        self.file = config_file
        self.debug_mode = False
        self.echo_mode = False
        self.db_dialect = ''
        self.is_user_request = False
        self.read_config()

    def read_config(self):
        config_data = ini_to_dict(self.file.path)
        self.echo_mode = True if config_data['DATABASE']['echo'] == 'True' else False
        self.debug_mode = True if config_data['APPLICATION']['debug_mode'] == 'True' else False
        self.db_dialect = config_data['DATABASE']['dialect']


class Database:

    def __init__(self, dialect: str, db_file_path: str, echo_mode: bool):
        self.file = File(db_file_path)
        self.uri = '{}:///{}'.format(dialect, self.file.path)
        self.connection = Connection(self.uri, echo_mode)

    def __repr__(self):
        return self.file.path

    @property
    def session(self):
        return self.connection.session


class Storage(Root):

    def __init__(self, root: Directory):
        super().__init__(root)
        self.answers = self.root.add_dir('answers')
        self.imports = self.root.add_dir('defenders')
        self.eskk = self.root.add_dir('eskk')
        self.exports = self.root.add_dir('exports')
        self.images = Images(self.root.add_dir('images'))
        self.orders = self.root.add_dir('orders')


class Eskk(Root):

    def __init__(self, root: Directory):
        super().__init__(root)
        self.genders = File(self.root.add_file('genders.csv'))
        self.document_types = File(self.root.add_file('document_types.csv'))
        self.military_ranks = File(self.root.add_file('military_ranks.csv'))
        self.military_subjects = File(self.root.add_file('military_subjects.csv'))

    def genders_data(self):
        return csv_to_dict(self.genders) if self.genders.is_exists else []

    def document_types_data(self):
        return csv_to_dict(self.document_types) if self.document_types.is_exists else []

    def military_ranks_data(self):
        return csv_to_dict(self.military_ranks) if self.military_ranks.is_exists else []

    def military_subjects_data(self):
        return csv_to_dict(self.military_subjects) if self.military_subjects.is_exists else []


class Images(Root):

    def __init__(self, root: Directory):
        super().__init__(root)
        self.icon = self.root.add_file('icon.ico')
        self.delete = self.root.add_file('delete.png')
        self.finish = self.root.add_file('finish.png')
        self.import_p = self.root.add_file('import_p.png')
        self.init_p = self.root.add_file('init_p.png')
        self.open = self.root.add_file('open.png')
        self.refresh = self.root.add_file('refresh.png')
        self.result = self.root.add_file('result.png')
        self.undo = self.root.add_file('undo.png')
        self.folder = self.root.add_file('folder.png')
        self.rosgvard = self.root.add_file('rg.png')
