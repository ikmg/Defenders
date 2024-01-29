from backend import DefendersApp
from backend import ImportUploader, OrdersUploader


app = DefendersApp()


# ЗАЩИТНИКИ

file_path = 'storage/test/test.xlsx'
subject_id = '1'
sheet_name = 'Лист1'

# try после выбора файла
loader = ImportUploader(app.database.session, subject_id, file_path)
loader.workbook.load()
loader.workbook.select_worksheet(sheet_name)
# try после нажать кнопку загрузить
loader.workbook.check_active_worksheet()
destination = app.storage.imports.add_dir(subject_id).add_file(loader.storage_filename)
loader.upload(destination.path, '1')


# ПРИКАЗЫ

file_path = '/home/kmg/PycharmProjects/Defenders/storage/orders/20240110-145510.xlsx'

# try после выбора файла
loader = OrdersUploader(app.database.session, file_path)
loader.workbook.load()
# try после нажать кнопку загрузить
destination = app.storage.orders.add_file(loader.storage_filename)
loader.upload(destination.path)
