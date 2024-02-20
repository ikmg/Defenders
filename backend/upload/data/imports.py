from .base import BaseWorkbook
from tools import DTConvert


class ImportWorkbook(BaseWorkbook):
    """
    Класс получения данных из поступающих файлов от войск
    """

    def check_active_worksheet(self):
        """
        Проверка соответствия шаблону
        """
        min_row_count = 3
        min_col_count = 37
        if self.max_row_num < min_row_count:  # минимально допустимое количество строк
            raise ValueError('количество строк меньше {}'.format(min_row_count))
        if len(self.get_row_num_data(1)) < min_col_count:  # минимально допустимое количество столбцов
            raise ValueError('количество столбцов меньше {}'.format(min_col_count))

    def worksheet_data(self):
        """
        Сбор полезных данных
        """
        result = []
        for row_num in range(3, self.max_row_num + 1):  # начиная со строки № 3
            row_val = self.get_row_num_data(row_num)[:37]  # отбор 37 столбцов по номеру строки
            if row_val[0]:  # если первая ячейка в строке не пустая
                result.append(row_to_dict(row_num, row_val))
            else:
                break
        if result:
            return result
        else:
            raise ValueError('данные отсутствуют')


def row_to_dict(row_num, row_val):
    """Преобразование строки с данными в словарь"""
    result = {
        'record': {
            'keep_row_num': row_num - 2,
            'file_row_num': row_num
        },
        'defender': {
            'person': {
                'last_name': row_val[0],
                'first_name': row_val[1],
                'middle_name': row_val[2],
                'eskk_gender_id': row_val[3],
                'birthday': DTConvert(row_val[4]).dstring,  # должна быть дата
                'snils': row_val[6]
            },
            'birth_place': row_val[5],
            'document': {
                'eskk_document_type_id': row_val[7],
                'serial': row_val[8],
                'number': row_val[9],
                'date': DTConvert(row_val[10]).dstring,  # должна быть дата
                'organization': row_val[11]
            },
            'document_vbd': {
                'serial': row_val[12],
                'number': row_val[13],
                'date': DTConvert(row_val[14]).dstring,  # должна быть дата
                'organization': row_val[15]
            },
            'reg_address': {
                'index': row_val[16],
                'region': row_val[17],
                'area': row_val[18],
                'locality': row_val[19],
                'street': row_val[20],
                'house': row_val[21],
                'building': row_val[22],
                'flat': row_val[23]
            },
            'fact_address': {
                'index': row_val[24],
                'region': row_val[25],
                'area': row_val[26],
                'locality': row_val[27],
                'street': row_val[28],
                'house': row_val[29],
                'building': row_val[30],
                'flat': row_val[31]
            },
            'id_ern': row_val[32],
            'subject_name': row_val[33],
            'exclude_date': DTConvert(row_val[34]).dstring,  # должна быть дата
            'exclude_order': row_val[35],
            'personal_number': row_val[36]
        }
    }
    return result
