from datetime import datetime

from database import KeepedReport, KeepedReportRecord
from tools import datetime_to_string


def defenders_load_data(session, import_id):
    data = [
        [
            'Дата импорта',
            'Субъект войск',
            'Рег. номер импорта',
            'Дата формирования',
            'Загружен',
            'Примечание'
        ]
    ]
    report = session.query(KeepedReport).filter(KeepedReport.id == import_id).scalar()
    row = [
        datetime_to_string(report.created_utc),
        report.eskk_military_subject.short_name,
        report.id,
        datetime_to_string(datetime.now()),
        'Да' if report.is_loaded else 'Нет',
        report.note
    ]
    data.append(row)
    return data


def defenders_identify_data(session, import_id):
    data = [
        [
            'Номер п/п',
            'Строка в файле',
            'ФИО',
            'Дата рождения',
            'Дата импорта',
            'Предупреждения',
            'Критические ошибки'
        ]
    ]
    defenders = session.query(KeepedReportRecord)
    defenders = defenders.filter(KeepedReportRecord.keeped_report_id == import_id)
    defenders = defenders.order_by(KeepedReportRecord.keep_row_num)
    defenders = defenders.all()

    for defender in defenders:
        row = [
            defender.keep_row_num,
            defender.file_row_num,
            defender.linked_defender.linked_person.person_appeal,
            defender.linked_defender.linked_person.birthday,
            datetime_to_string(defender.created_utc),
            defender.warning_messages,
            defender.critical_messages
        ]
        data.append(row)

    data.append([])
    data.append([
        'Контакты',
        defenders[0].keeped_report.contact_info
    ])
    q = 1

    return data
