from datetime import datetime

from database import KeepedReport, KeepedReportRecord
from tools.date_time import DateTimeConvert


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
        DateTimeConvert(report.created_utc).string,  # должно быть дата/время
        report.eskk_military_subject.short_name,
        report.id,
        DateTimeConvert(datetime.now()).string,  # должно быть дата/время
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
            DateTimeConvert(defender.created_utc).string,  # должно быть дата/время
            defender.warning_messages,
            defender.critical_messages
        ]
        data.append(row)

    data.append([])
    data.append([
        'Контакты',
        defenders[0].keeped_report.contact_info
    ])

    return data
