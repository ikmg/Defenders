from database import LinkedPerson, LinkedDefender, PickedLastName, PickedFirstName, PickedMiddleName, KeepedReportRecord


def get_persons(session):
    persons = session.query(LinkedPerson)
    persons = persons.join(PickedLastName)
    persons = persons.join(PickedFirstName)
    persons = persons.join(PickedMiddleName)
    persons = persons.order_by(PickedLastName.value, PickedFirstName.value, PickedMiddleName.value)
    persons = persons.all()
    return persons


def get_sfr_control_rows(session):
    rows = []
    row_number = 0
    persons = get_persons(session)
    for person in persons:
        if person.linked_defenders:
            person_data = [
                person.picked_last_name.value,
                person.picked_first_name.value,
                person.picked_middle_name.value,
                person.eskk_gender.name,
                person.birthday,
                person.picked_snils.value
            ]

            defenders = []
            for defender in person.linked_defenders:
                if defender.keeped_report_records:
                    defenders.append(defender)

            answers = []
            if defenders:
                answers = get_answers(defenders)

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
    for defender in defenders:
        for keeped_report_record in defender.keeped_report_records: # обработка каждой записи, т.к. может отправляться неоднократно
            if keeped_report_record.provided_report_record:  # отправленные записи

                result['doc_type'] = '{}{}\n'.format(
                    result['doc_type'],
                    defender.linked_document.eskk_document_type.name
                )

                result['doc_ser'] = '{}{}\n'.format(
                    result['doc_ser'],
                    defender.linked_document.picked_serial.value
                )

                result['doc_num'] = '{}{}\n'.format(
                    result['doc_num'],
                    defender.linked_document.picked_number.value
                )

                result['doc_org'] = '{}{}\n'.format(
                    result['doc_org'],
                    defender.linked_document.picked_organization.value
                )

                result['send'] = '{}{}\n'.format(
                    result['send'],
                    keeped_report_record.provided_report_record.provided_report.created_utc.date()
                )

                result['reg_num'] = '{}{} строка {}\n'.format(
                    result['reg_num'],
                    keeped_report_record.provided_report_record.provided_report_id,
                    keeped_report_record.provided_report_record.row_number
                )

                if keeped_report_record.provided_report_record.answer_init:  # если ответ поступил
                    result['answer'] = '{}{}\n'.format(
                        result['answer'],
                        keeped_report_record.provided_report_record.answer_init.comment
                    )
                else:
                    result['answer'] = '{}{}\n'.format(
                        result['answer'],
                        'Не поступал'
                    )
    # если ответ содержит необходимые слова
    if 'загружены' in result['answer'] or 'добавлен' in result['answer'] or 'Не поступал' in result['answer']:
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
