import csv


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
