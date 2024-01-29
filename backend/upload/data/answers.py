from .base import BaseWorkbook


class AnswerWorkbook(BaseWorkbook):

    def check_active_worksheet(self):
        pass

    def worksheet_data(self):
        pass


# from .workbook import Workbook
#
#
# class SfrImportWorkbook(Workbook):
#
#     def check(self):
#         pass
#
#     def read_import(self):
#         try:
#             wb = openpyxl.load_workbook(self.import_filename)
#             ws = wb.active
#             self.answer['import_data'] = {
#                 'import_date': string_to_date(ws['B3'].value),
#                 'reg_number': ws['B4'].value,
#                 'user': ws['B5'].value,
#                 'result': ws['B9'].value
#             }
#         except:
#             self.messages.append('ошибка чтения протокола загрузки {}'.format(self.import_filename))
#             self.answer['import_data'] = None
#
#
# class SfrInitWorkbook(Workbook):
#
#     def check(self):
#         pass
#
#     def read_init(self):
#         try:
#             wb = openpyxl.load_workbook(self.init_filename)
#             ws = wb.active
#             for index, row in enumerate(ws.iter_rows()):
#                 if index >= 1 and row[0].value:
#                     record = {
#                         'number': int(row[0].value),
#                         'fio': row[1].value.replace(u'\ufeff', '', 1),
#                         'birthday': string_to_date(row[2].value),
#                         'init_date': string_to_datetime(row[3].value),
#                         'status': row[4].value if row[4].value else '',
#                         'comment': row[5].value if row[5].value else '',
#                         'provided_report_record_id': None
#                     }
#                     self.answer['init_data'].append(record)
#         except:
#             self.messages.append('ошибка чтения протокола идентификации {}'.format(self.init_filename))
#             self.answer['init_data'] = []
