from database import Connection, DefenderParameter
from backend import dict_from_ini
from backend import eskk_genders_upload, eskk_document_types_upload, eskk_military_ranks_upload, eskk_military_subjects_upload

from tools.filesystem import Directory, File, work_directory
from tools.date_time import DateTimeConvert


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

    def eskk_update_all(self):
        self.eskk_update_genders()
        self.eskk_update_document_types()
        self.eskk_update_military_ranks()
        self.eskk_update_document_types()

    def eskk_update_genders(self):
        eskk_genders_upload(self.database.session, self.storage.eskk.genders.path)

    def eskk_update_document_types(self):
        eskk_document_types_upload(self.database.session, self.storage.eskk.document_types.path)

    def eskk_update_military_ranks(self):
        eskk_military_ranks_upload(self.database.session, self.storage.eskk.military_ranks.path)

    def eskk_update_military_subjects(self):
        eskk_military_subjects_upload(self.database.session, self.storage.eskk.military_subjects.path)

    def print_log(self, text: str):
        log_row = [DateTimeConvert().string, text]
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
        config_data = dict_from_ini(self.file.path)
        self.echo_mode = True if config_data['DATABASE']['echo'] == 'True' else False
        self.debug_mode = True if config_data['APPLICATION']['debug_mode'] == 'True' else False
        self.db_dialect = config_data['DATABASE']['dialect']


class Database:

    def __init__(self, dialect: str, db_file_path: str, echo_mode: bool):
        self.file = File(db_file_path)
        self.uri = '{}:///{}'.format(dialect, self.file.path)
        self.connection = Connection(self.uri, echo_mode)
        self.connection.create_db()

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
        self.eskk = Eskk(self.root.add_dir('eskk'))
        self.exports = self.root.add_dir('exports')
        self.images = Images(self.root.add_dir('images'))
        self.orders = self.root.add_dir('orders')


class Eskk(Root):

    def __init__(self, root: Directory):
        super().__init__(root)
        self.genders = self.root.add_file('genders.csv')
        self.document_types = self.root.add_file('document_types.csv')
        self.military_ranks = self.root.add_file('military_ranks.csv')
        self.military_subjects = self.root.add_file('military_subjects.csv')


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
