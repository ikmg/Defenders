from database import KeepedOrderRecord
from tools import Application

app = Application()
session = app.db_connection.session

orders_periods = session.query(KeepedOrderRecord).all()

ln_set = set()
fn_set = set()
mn_set = set()

for period in orders_periods:
    if period.linked_order_person_period:
        fio = period.linked_order_person_period.linked_order_person.linked_order_fio
        if not fio.picked_last_name:
            ln_set.add(fio.picked_last_name_id)
        if not fio.picked_first_name:
            fn_set.add(fio.picked_first_name_id)
        if not fio.picked_middle_name:
            mn_set.add(fio.picked_middle_name_id)

print(len(ln_set), ln_set)
print(len(fn_set), fn_set)
print(len(mn_set), mn_set)
