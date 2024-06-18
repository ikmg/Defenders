from database import LinkedPerson, PickedLastName, PickedFirstName, PickedMiddleName
from tools import DTConvert


def get_persons(session):
    """
    Получение уникальных персон из базы
    """
    persons = session.query(LinkedPerson)
    persons = persons.join(PickedLastName)
    persons = persons.join(PickedFirstName)
    persons = persons.join(PickedMiddleName)
    persons = persons.order_by(PickedLastName.value, PickedFirstName.value, PickedMiddleName.value)
    persons = persons.all()
    return persons


def get_sfr_control_rows(session):
    """
    Получение строк для сверки с СФР.
    Защитник должен быть идентифицирован в СФР,
    либо в настоящий момент не имеет ответа от СФР
    """
    rows = []
    row_number = 0
    persons = get_persons(session)
    for person in persons:
        if person.linked_defenders:  # если с персоной связан защитник
            # установочные данные о персоне
            person_data = [
                person.picked_last_name.value,
                person.picked_first_name.value,
                person.picked_middle_name.value,
                person.eskk_gender.name,
                person.birthday,
                person.picked_snils.value
            ]
            # сбор защитников у персоны
            defenders = []
            for defender in person.linked_defenders:
                if defender.keeped_report_records:  # если у защитника есть хранимая запись
                    defenders.append(defender)
            # сбор ответов по защитников от СФР
            answers = []
            if defenders:
                answers = get_answers(defenders)
            # если ответы есть, добавляем строку
            if answers:
                row_number += 1
                rows.append([row_number] + person_data + answers)

    return rows


def get_answers(defenders):
    # результат
    result = {
        'doc_type': '',
        'doc_ser': '',
        'doc_num': '',
        'doc_org': '',
        'send': '',  # дата отправки
        'reg_num': '',  # регистрационный номер отправки
        'answer': ''  # ответ СФР
    }
    for defender in defenders:  # для каждого полученного защитника
        for keeped_report_record in defender.keeped_report_records:  # обработка каждой хранимой записи
            if keeped_report_record.provided_report_record:  # если запись была выгружена
                # тип документа
                result['doc_type'] = '{}{}\n'.format(
                    result['doc_type'],
                    defender.linked_document.eskk_document_type.name
                )
                # серия документа
                result['doc_ser'] = '{}{}\n'.format(
                    result['doc_ser'],
                    defender.linked_document.picked_serial.value
                )
                # номер документа
                result['doc_num'] = '{}{}\n'.format(
                    result['doc_num'],
                    defender.linked_document.picked_number.value
                )
                # кто выдал документ
                result['doc_org'] = '{}{}\n'.format(
                    result['doc_org'],
                    defender.linked_document.picked_organization.value
                )
                # дата выгрузки
                result['send'] = '{}{}\n'.format(
                    result['send'],
                    DTConvert(
                        keeped_report_record.provided_report_record.provided_report.created_utc.date()
                    ).dstring
                )
                # регистрационный номер выгрузки и номер строки в выгрузке
                result['reg_num'] = '{}{}, строка {}\n'.format(
                    result['reg_num'],
                    keeped_report_record.provided_report_record.provided_report_id,
                    keeped_report_record.provided_report_record.row_number
                )
                # если на выгруженную запись поступил ответ от СФР
                if keeped_report_record.provided_report_record.answer_init:
                    # добавляем ответ
                    result['answer'] = '{}{}\n'.format(
                        result['answer'],
                        keeped_report_record.provided_report_record.answer_init.comment
                    )
                else:  # если ответ от СФР не поступил
                    result['answer'] = '{}{}\n'.format(
                        result['answer'],
                        'Не поступал'
                    )
    # если результат содержит необходимые слова
    if (
            'загружены' in result['answer'] or
            'добавлен' in result['answer'] or
            'Не поступал' in result['answer']
    ):
        return [
            result['doc_type'],
            result['doc_ser'],
            result['doc_num'],
            result['doc_org'],
            result['send'],
            result['reg_num'],
            result['answer']
        ]
    else:
        return None
