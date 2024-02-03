import csv


def csv_from_dict(filename, headers, data_dict):
    with open(filename, 'w', encoding='utf-8') as report:
        writer = csv.DictWriter(report, fieldnames=headers, dialect='excel', delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data_dict)


def csv_from_list(filename, data_list):
    with open(filename, 'w', encoding='utf-8', newline='') as report:
        writer = csv.writer(report, dialect='excel', delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerows(data_list)
