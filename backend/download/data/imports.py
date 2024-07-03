import json

from database import KeepedReport, KeepedReportRecord
from tools import DTConvert


def protocol_import_data(session, import_id):
    """Данные для формирования файла с протоколом загрузки"""
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
        DTConvert(report.created_utc).dtstring,  # должно быть дата/время
        report.eskk_military_subject.short_name,
        report.id,
        DTConvert().dtstring,  # должно быть дата/время
        'Да' if report.is_loaded else 'Нет',
        report.note
    ]
    data.append(row)
    return data


def protocol_init_data(session, import_id):
    """Данные для формирования файла с протоколом идентификации"""
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
    records = session.query(KeepedReportRecord)
    records = records.filter(KeepedReportRecord.keeped_report_id == import_id)
    records = records.order_by(KeepedReportRecord.keep_row_num)
    records = records.all()

    for record in records:
        row = [
            record.keep_row_num,
            record.file_row_num,
            record.linked_defender.linked_person.person_appeal,
            record.linked_defender.linked_person.birthday,
            DTConvert(record.created_utc).dtstring,  # должно быть дата/время
            record.warning_messages,
            record.critical_messages
        ]
        data.append(row)

    data.append([])
    data.append([
        'Контакты',
        records[0].keeped_report.contact_info
    ])

    return data


def result_file_data(session, import_id):
    # TODO запрашивать информацию из базы данных по номеру импорта, дополнять колонкой 38
    report = session.query(KeepedReport)
    report = report.join(KeepedReportRecord)
    report = report.filter(KeepedReportRecord.keeped_report_id == import_id)
    report = report.order_by(KeepedReportRecord.keep_row_num)
    report = report.scalar()
    data = [
        {
            'data': [
                'Номер п/п',
                'Строка в файле',
                'Фамилия',
                'Имя',
                'Отчество (при наличии)',
                'Пол',
                'Дата рождения',
                'Место рождения',
                'СНИЛС',
                'Вид документа',
                'Серия',
                'Номер',
                'Дата выдачи',
                'Орган, выдавший документ, удостоверяющий личность',
                'Серия',
                'Номер',
                'Дата выдачи',
                'Наименование органа, выдавшего документ',
                'Почтовый индекс места жительства',
                'Регион места жительства',
                'Район места жительства',
                'Населенный пункт места жительства',
                'Улица места жительства',
                'Дом места жительства',
                'Корпус/строение места жительства',
                'Квартира места жительства',
                'Почтовый индекс места пребывания',
                'Регион места пребывания',
                'Район места пребывания',
                'Населенный пункт места пребывания',
                'Улица места пребывания',
                'Дом места пребывания',
                'Корпус/строение места пребывания',
                'Квартира места пребывания',
                'ID ЕРН',
                'Воинская часть (подразделение)',
                'Дата исключения',
                'Номер и дата приказа об исключения',
                'Личный номер',
                'РЕЗУЛЬТАТ'
            ],
            'warnings': {},
            'critical': {}
        },
        {
            'data': [
                '---',
                '---',
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8',
                '9',
                '10',
                '11',
                '12',
                '13',
                '14',
                '15',
                '16',
                '17',
                '18',
                '19',
                '20',
                '21',
                '22',
                '23',
                '24',
                '25',
                '26',
                '27',
                '28',
                '29',
                '30',
                '31',
                '32',
                '33',
                '34',
                '35',
                '36',
                '37',
                '---'
            ],
            'warnings': {},
            'critical': {}
        }
    ]
    for record in report.keeped_report_records:
        defender = record.linked_defender
        person = defender.linked_person
        document = defender.linked_document
        document_vbd = defender.linked_document_vbd
        reg_address = defender.linked_reg_address
        fact_address = defender.linked_fact_address
        row = [
            record.keep_row_num,
            record.file_row_num,
            person.picked_last_name.value,
            person.picked_first_name.value,
            person.picked_middle_name.value,
            person.eskk_gender.id,
            person.birthday,
            defender.birth_place,
            person.picked_snils.value,
            document.eskk_document_type.id,
            document.picked_serial.value,
            document.picked_number.value,
            document.date,
            document.picked_organization.value,
            document_vbd.picked_serial.value,
            document_vbd.picked_number.value,
            document_vbd.date,
            document_vbd.picked_organization.value,
            reg_address.picked_index.value,
            reg_address.picked_region.value,
            reg_address.picked_area.value,
            reg_address.picked_locality.value,
            reg_address.picked_street.value,
            reg_address.picked_house.value,
            reg_address.picked_building.value,
            reg_address.picked_flat.value,
            fact_address.picked_index.value,
            fact_address.picked_region.value,
            fact_address.picked_area.value,
            fact_address.picked_locality.value,
            fact_address.picked_street.value,
            fact_address.picked_house.value,
            fact_address.picked_building.value,
            fact_address.picked_flat.value,
            defender.id_ern,
            defender.picked_military_subject.value,
            defender.exclude_date,
            defender.exclude_order,
            defender.picked_personal_number.value
        ]
        if not record.is_find_in_orders:
            row.append('ОШИБКА: отсутствует в приказах ОШУ Росгвардии')
        elif record.critical_messages:
            row.append('КРИТИЧЕСКИЕ ОШИБКИ: {}'.format(record.critical_messages))
        elif not record.provided_report_record.answer_init:
            row.append('Ответ СФР: не поступал')
        else:
            row.append('Ответ СФР: {}'.format(record.provided_report_record.answer_init.comment))
        data.append({
            'data': row,
            'warnings': json.loads(record.warning_colors) if record.warning_colors else {},
            'critical': json.loads(record.critical_colors) if record.critical_colors else {}
        })
    data.append({
        'data': [],
        'warnings': {},
        'critical': {}
    })
    data.append({
        'data': ['Контакты', report.contact_info],
        'warnings': {},
        'critical': {}
    })
    return data
