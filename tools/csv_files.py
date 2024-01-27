import csv


def csv_to_dict(filename):
    result = []
    with open(filename, encoding='utf-8') as csv_file:
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


def write_csv_dict(filename, headers, data_dict):
    """

    :param filename:
    :param headers:
    :param data_dict:
    :return:
    """
    with open(filename, 'w', encoding='utf-8') as report:
        writer = csv.DictWriter(report, fieldnames=headers, dialect='excel', delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data_dict)


def write_csv_list(filename, data_list):
    """

    :param filename:
    :param data_list:
    :return:
    """
    with open(filename, 'w', encoding='utf-8', newline='') as report:
        writer = csv.writer(report, dialect='excel', delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerows(data_list)
