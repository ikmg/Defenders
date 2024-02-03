import csv

from tools import File


def dict_from_csv(file_path):
    file = File(file_path)
    if not file.is_exists:
        raise FileNotFoundError('файл <{}> не существует'.format(file.path))

    result = []
    with open(file.path, encoding='utf-8') as csv_file:
        data = csv.reader(csv_file)
        headers = []
        for row_ind, row_val in enumerate(data):
            if row_ind == 0:
                headers = row_val
            else:
                dict_row = {}
                for col_ind, col_val in enumerate(row_val):
                    dict_row[headers[col_ind]] = col_val
                result.append(dict_row)
    return result
