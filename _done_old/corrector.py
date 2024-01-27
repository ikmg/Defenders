from datetime import datetime
from uuid import uuid4

from sqlalchemy.sql.operators import ilike_op

from database import PickedLastName, PickedFirstName, PickedMiddleName, LinkedPerson, LinkedOrderFIO, KeepedReportRecord, LinkedOrderPerson, PickedPersonalNumber
from tools import Application, change_e_symbol


app = Application()
session = app.db_connection.session

count = 0
print('\nФАМИЛИЯ')
old_models = session.query(PickedLastName).all()
for old_model in old_models:
    if 'Ё' in old_model.value or 'ё' in old_model.value:
        count += 1
        message = '#{}: <{}>'.format(count, old_model.value)

        new_value = change_e_symbol(old_model.value)
        new_model = session.query(PickedLastName).filter(PickedLastName.value == new_value).scalar()
        message = '{} -> <{}>'.format(message, new_value)

        if not new_model:
            message = '{} ({})'.format(message, 'исправление значение')
            old_model.value = new_value
            session.flush()
        else:
            message = '{} ({})'.format(message, 'замена ИД')
            # new_model = PickedLastName()
            # new_model.id = str(uuid4())
            # new_model.created_utc = datetime.now()
            # new_model.value = new_value
            # session.add(new_model)
            # session.flush()

            count_defenders = 0
            persons = session.query(LinkedPerson).filter(LinkedPerson.picked_last_name_id == old_model.id).all()
            for person in persons:
                person.picked_last_name_id = new_model.id
                session.flush()

            fios = session.query(LinkedOrderFIO).filter(LinkedOrderFIO.picked_last_name_id == old_model.id).all()
            for fio in fios:
                fio.picked_last_name_id = new_model.id
                session.flush()

            message = '{} защитники - {}, приказы - {}'.format(message, len(persons), len(fios))
        print(message)

count = 0
print('\nИМЯ')
old_models = session.query(PickedFirstName).all()
for old_model in old_models:
    if 'Ё' in old_model.value or 'ё' in old_model.value:
        count += 1
        message = '#{}: <{}>'.format(count, old_model.value)

        new_value = change_e_symbol(old_model.value)
        new_model = session.query(PickedFirstName).filter(PickedFirstName.value == new_value).scalar()
        message = '{} -> <{}>'.format(message, new_value)

        if not new_model:
            message = '{} ({})'.format(message, 'исправление значение')
            old_model.value = new_value
            session.flush()
        else:
            message = '{} ({})'.format(message, 'замена ИД')
            # new_model = PickedFirstName()
            # new_model.id = str(uuid4())
            # new_model.created_utc = datetime.now()
            # new_model.value = new_value
            # session.add(new_model)
            # session.flush()

            count_defenders = 0
            persons = session.query(LinkedPerson).filter(LinkedPerson.picked_first_name_id == old_model.id).all()
            for person in persons:
                person.picked_first_name_id = new_model.id
                session.flush()

            fios = session.query(LinkedOrderFIO).filter(LinkedOrderFIO.picked_first_name_id == old_model.id).all()
            for fio in fios:
                fio.picked_first_name_id = new_model.id
                session.flush()

            message = '{} защитники - {}, приказы - {}'.format(message, len(persons), len(fios))
        print(message)

count = 0
print('\nОТЧЕСТВО')
old_models = session.query(PickedMiddleName).all()
for old_model in old_models:
    if 'Ё' in old_model.value or 'ё' in old_model.value:
        count += 1
        message = '#{}: <{}>'.format(count, old_model.value)

        new_value = change_e_symbol(old_model.value)
        new_model = session.query(PickedMiddleName).filter(PickedMiddleName.value == new_value).scalar()
        message = '{} -> <{}>'.format(message, new_value)

        if not new_model:
            message = '{} ({})'.format(message, 'исправление значение')
            old_model.value = new_value
            session.flush()
        else:
            message = '{} ({})'.format(message, 'замена ИД')
            # new_model = PickedMiddleName()
            # new_model.id = str(uuid4())
            # new_model.created_utc = datetime.now()
            # new_model.value = new_value
            # session.add(new_model)
            # session.flush()

            count_defenders = 0
            persons = session.query(LinkedPerson).filter(LinkedPerson.picked_middle_name_id == old_model.id).all()
            for person in persons:
                person.picked_middle_name_id = new_model.id
                session.flush()

            fios = session.query(LinkedOrderFIO).filter(LinkedOrderFIO.picked_middle_name_id == old_model.id).all()
            for fio in fios:
                fio.picked_middle_name_id = new_model.id
                session.flush()

            message = '{} защитники - {}, приказы - {}'.format(message, len(persons), len(fios))
        print(message)

count = 0
print('\nПОВТОРНЫЙ ПОИСК ПО ПРИКАЗАМ')
models = session.query(KeepedReportRecord).filter(KeepedReportRecord.is_find_in_orders == False).order_by(KeepedReportRecord.created_utc).all()
print('обработка {}...'.format(len(models)))
for index, model in enumerate(models):
    try:
        order_fio = session.query(LinkedOrderFIO).filter(
            LinkedOrderFIO.picked_last_name_id == model.linked_defender.linked_person.picked_last_name.id,
            LinkedOrderFIO.picked_first_name_id == model.linked_defender.linked_person.picked_first_name.id,
            LinkedOrderFIO.picked_middle_name_id == model.linked_defender.linked_person.picked_middle_name.id
        ).scalar()
    except:
        order_fio = None

    order_persons = session.query(LinkedOrderPerson).join(PickedPersonalNumber).filter(
        ilike_op(PickedPersonalNumber.value, '%{}%'.format(model.linked_defender.picked_personal_number.value))
    ).all()

    if order_fio:
        if order_persons:
            for order_person in order_persons:
                if order_person.linked_order_fio_id == order_fio.id:
                    count += 1
                    model.is_find_in_orders = True
                    session.flush()

print('Найдено в приказах {} из {}'.format(count, len(models)))
session.commit()
