from database import LinkedPerson, LinkedDefender, PickedLastName, PickedFirstName, PickedMiddleName, KeepedReportRecord


def get_defenders(session):
    defenders = session.query(LinkedDefender)
    defenders = defenders.join(LinkedPerson)
    defenders = defenders.join(PickedLastName)
    defenders = defenders.join(PickedFirstName)
    defenders = defenders.join(PickedMiddleName)
    defenders = defenders.order_by(PickedLastName.value, PickedFirstName.value, PickedMiddleName.value)
    defenders = defenders.all()
    return defenders


def get_sfr_control_rows(session):
    rows = []
    count = 0
    defenders = get_defenders(session)
    defender: LinkedDefender
    for defender in defenders:
        row = [
            defender.linked_person.picked_last_name.value,
            defender.linked_person.picked_first_name.value,
            defender.linked_person.picked_middle_name.value,
            defender.linked_person.eskk_gender.name,
            defender.linked_person.birthday,
            defender.linked_person.picked_snils.value,
            defender.linked_document.eskk_document_type.name,
            defender.linked_document.picked_serial.value,
            defender.linked_document.picked_number.value,
            defender.linked_document.picked_organization.value,
        ]

        if defender.keeped_report_records:
            answers = get_answers(defender.keeped_report_records)
            if answers:
                count += 1
                row += answers
                rows.append([count] + row)
        # else:
        #     row.append('Кто ты?')
        #     row.append('---')
        # rows.append(row)
    return rows


def get_answers(records):
    # результат
    result = {
        'send': '',  # дата отправки
        'answer': ''  # ответ СФР
    }
    record: KeepedReportRecord
    for record in records:  # обработка каждой записи, т.к. может отправляться неоднократно
        if record.provided_report_record:  # отправленные записи
            result['send'] = '{}{}\n'.format(result['send'], record.provided_report_record.provided_report.created_utc.date())
            if record.provided_report_record.answer_init:  # если ответ поступил
                result['answer'] = '{}{}\n'.format(result['answer'], record.provided_report_record.answer_init.comment)
            else:
                result['answer'] = '{}{}\n'.format(result['answer'], 'Не поступал')
    # если ответ содержит необходимые слова
    if 'загружены' in result['answer'] or 'добавлен' in result['answer'] or 'Не поступал' in result['answer']:
        return [result['send'], result['answer']]
    else:
        return None
