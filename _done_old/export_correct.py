from database import ProvidedReport
from tools import Application

app = Application()
session = app.db_connection.session

export = session.query(ProvidedReport).filter(ProvidedReport.id == '3203-20231121-153907').scalar()
for record in export.provided_report_records:
    # print(
    #     record.keeped_report_record.keep_row_num, ';',
    #     record.keeped_report_record.linked_defender.linked_person.person_appeal, ';',
    #     record.keeped_report_record.linked_defender.linked_person.birthday
    # )

    if record.row_number in [
        93,
        107,
        119,
        120,
        124,
        151,
        82,
        543,
        521,
        165,
        174,
        197,
        208,
        226
    ]:
        q = 1
        print(
            record.id, ';',
            record.keeped_report_record.keep_row_num, ';',
            record.keeped_report_record.linked_defender.linked_person.person_appeal, ';',
            record.keeped_report_record.linked_defender.linked_person.birthday
        )
