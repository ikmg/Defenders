from sqlalchemy.sql.operators import like_op

from database import Connection, vacuum_db, patch_db, DefenderParameter, LinkedPerson, KeepedReport
from backend import dict_from_ini
from backend import eskk_genders_upload, eskk_document_types_upload, eskk_military_ranks_upload, eskk_military_subjects_upload

from tools import Directory, File, work_directory, DTConvert

# НАЗВАНИЯ ВЕРСИЙ - НАЗВАНИЯ ОРУДИЙ - ПО АЛФАВИТУ
# А - АЛЕБАРДА
# Б - БЕРДАНКА
# В - ВИНТОВКА
# Г - ГАРДА
APP_VERSION = 'АЛЕБАРДА'
APP_RELEASE = '21.03.2024'


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
            self.storage.root.add_file('defenders.db'),
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
        eskk_genders_upload(self.database.session, self.storage.eskk.genders)

    def eskk_update_document_types(self):
        eskk_document_types_upload(self.database.session, self.storage.eskk.document_types)

    def eskk_update_military_ranks(self):
        eskk_military_ranks_upload(self.database.session, self.storage.eskk.military_ranks)

    def eskk_update_military_subjects(self):
        eskk_military_subjects_upload(self.database.session, self.storage.eskk.military_subjects)

    def print_log(self, text: str):
        log_row = [DTConvert().dtstring, text]
        self.log.append(log_row)
        if self.settings.debug_mode:
            print(' '.join(log_row))

    @property
    def version(self):
        return 'v. {} {}'.format(
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

    def __init__(self, dialect: str, db_file: File, echo_mode: bool):
        self.file = db_file
        self.uri = '{}:///{}'.format(dialect, self.file.path)
        self.connection = Connection(self.uri, echo_mode)
        self.connection.create_db()
        if not self.check_db():
            self.patcher()

    def __repr__(self):
        return self.file.path

    @property
    def session(self):
        return self.connection.session

    def vacuum(self):
        vacuum_db(self.file.path)

    def check_db(self):
        try:
            self.session.query(KeepedReport).first()
            return True
        except:
            return False

    def patcher(self):
        # патч структуры базы данных
        patch_db(self.file.path)
        self.check_db()

        # патч наличия времени в дате рождения
        models = self.session.query(LinkedPerson).filter(like_op(LinkedPerson.birthday, '% 00:00:00')).all()
        if models:
            for model in models:
                birthday = DTConvert(model.birthday).dstring
                model_exists = self.session.query(LinkedPerson).filter(
                    LinkedPerson.picked_snils_id == model.picked_snils_id,
                    LinkedPerson.picked_last_name_id == model.picked_last_name_id,
                    LinkedPerson.picked_first_name_id == model.picked_first_name_id,
                    LinkedPerson.picked_middle_name_id == model.picked_middle_name_id,
                    LinkedPerson.birthday == birthday
                ).scalar()
                if model_exists:
                    print('FUCKING SHIT! Linked person id: <{}>, birthday {} already exists as id <{}>'.format(model.id, birthday, model_exists.id))
                else:
                    model.birthday = birthday
        self.session.commit()


class Storage(Root):

    def __init__(self, root: Directory):
        super().__init__(root)
        self.answers = self.root.add_dir('answers')
        self.imports = self.root.add_dir('defenders')
        self.eskk = Eskk(self.root.add_dir('eskk'))
        self.exports = self.root.add_dir('export')
        self.images = Images(self.root.add_dir('images'))
        self.orders = self.root.add_dir('orders')
        self.stat = self.root.add_dir('stat')


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
        self.clear = self.root.add_file('clear.png')
        self.defenders = self.root.add_file('defenders.png')
        self.delete = self.root.add_file('delete.png')
        self.exports = self.root.add_file('exports.png')
        self.find = self.root.add_file('find.png')
        self.finish = self.root.add_file('finish.png')
        self.folder_open = self.root.add_file('folder_open.png')
        self.folder = self.root.add_file('folder.png')
        self.icon = self.root.add_file('icon.ico')
        self.import_p = self.root.add_file('import_p.png')
        self.imports = self.root.add_file('imports.png')
        self.info = self.root.add_file('info.png')
        self.init_p = self.root.add_file('init_p.png')
        self.load = self.root.add_file('load.png')
        self.menu = self.root.add_file('menu.png')
        self.open = self.root.add_file('open.png')
        self.orders = self.root.add_file('orders.png')
        self.properties = self.root.add_file('properties.png')
        self.refresh = self.root.add_file('refresh.png')
        self.result = self.root.add_file('result.png')
        self.search = self.root.add_file('search.png')
        self.tools = self.root.add_file('tools.png')
        self.stat = self.root.add_file('stat.png')
        self.undo = self.root.add_file('undo.png')
