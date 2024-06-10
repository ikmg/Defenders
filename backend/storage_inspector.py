from database import KeepedReport, KeepedOrder, ProvidedReport
from tools import Directory, File
from .application import DefendersApp


class FolderInspector:

    def __init__(self, dir: Directory):
        self.dir = dir
        self.fs_paths = self.get_files_paths()
        self.db_files = []
        self.outer_files = []

    def get_files_paths(self):
        files = self.dir.files_list()
        dirs = [Directory(x) for x in self.dir.dirs_list()]
        for dir in dirs:
            files += dir.files_list()
        return files

    def is_db_files_exists(self) -> bool:
        result = True
        for file in self.db_files:
            if not file.is_exists:
                result = False
                print('\t\tФайл отсутствует в хранилище <{}>'.format(file.path))
        return result

    def is_fs_files_in_db(self) -> bool:
        result = True
        db_files = [x.path for x in self.db_files]
        for file_path in self.fs_paths:
            if file_path not in db_files:
                result = False
                self.outer_files.append(File(file_path))
                print('\t\tФайл не учтен в базе данных <{}>'.format(file_path))
        return result

    def compare(self):
        print('\tПроверка наличия файлов в хранилище')
        if self.is_db_files_exists():
            print('\t\tOK')
        print('\tПроверка учета имеющихся файлов')
        if self.is_fs_files_in_db():
            print('\t\tOK')


class StorageInspector:

    def __init__(self, app: DefendersApp):
        self.imports = FolderInspector(app.storage.imports)
        self.orders = FolderInspector(app.storage.orders)
        self.exports = FolderInspector(app.storage.exports)

        self.imports.db_files = [File(x.instance_filename) for x in app.database.session.query(KeepedReport).order_by(KeepedReport.instance_filename).all()]
        self.orders.db_files = [File(x.instance_filename) for x in app.database.session.query(KeepedOrder).order_by(KeepedOrder.instance_filename).all()]
        export_ids = [x.id for x in app.database.session.query(ProvidedReport).order_by(ProvidedReport.id).all()]
        self.exports.db_files = [app.storage.exports.add_file('{}.csv'.format(x)) for x in export_ids]

    def compare(self):
        print('Анализ загрузок...')
        self.imports.compare()
        print('Анализ выгрузок...')
        self.exports.compare()
        print('Анализ приказов...')
        self.orders.compare()

    def clear(self):
        print('ОЧИСТКА НЕ ПРОИЗВОДИТСЯ. СКИНУТЬ ЛОГ')
