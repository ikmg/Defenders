from tools import DTConvert
from .base import BaseWorkbook


class AnswerImportWorkbook(BaseWorkbook):

    def check_active_worksheet(self):
        pass

    def worksheet_data(self):
        return {
            'date': DTConvert(self.get_row_num_data(3)[1]).date,
            'reg_num': self.get_row_num_data(4)[1],
            'user': self.get_row_num_data(5)[1],
            'result': self.get_row_num_data(9)[1]
        }


class AnswerInitWorkbook(BaseWorkbook):

    def check_active_worksheet(self):
        pass

    def worksheet_data(self):
        result = []
        for row_num in range(2, self.max_row_num + 1):  # начиная со строки № 2
            row_val = self.get_row_num_data(row_num)[:6]  # отбор 37 столбцов по номеру строки
            if row_val[0]:  # если первая ячейка в строке не пустая
                row = {
                    'number': int(row_val[0]),
                    'fio': row_val[1].replace(u'\ufeff', '', 1),
                    'birthday': DTConvert(row_val[2]).date,
                    'init_date': DTConvert(row_val[3]).datetime,
                    'status': row_val[4] if row_val[4] else '',
                    'comment': row_val[5] if row_val[5] else '',
                    'provided_report_record_id': None
                }
                result.append(row)
            else:
                break
        if result:
            return result
        else:
            raise ValueError('данные отсутствуют')
