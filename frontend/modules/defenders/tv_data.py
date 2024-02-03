from sqlalchemy import or_
from sqlalchemy.sql.operators import ilike_op

from database import LinkedDefender, LinkedPerson, PickedLastName, PickedFirstName, PickedMiddleName, PickedPersonalNumber


def _lower(arg: str) -> str:
    return arg.lower()


class DefenderData:

    def __init__(self, app):
        self.app = app
        self.model = None

    @property
    def session(self):
        return self.app.database.session

    def get_defender(self, defender_id):
        pass

    def table_model_row(self):
        answer = ''
        prot_sfr = '---'
        import_id = ''
        if self.model.keeped_report_records:
            for rec in self.model.keeped_report_records:
                if rec.provided_report_record:
                    if rec.provided_report_record.answer_init:
                        answer = 'Ответ СФР: {}'.format(rec.provided_report_record.answer_init.comment)
                        prot_sfr = rec.provided_report_record.provided_report.answer_import.reg_number
                    else:
                        answer = 'Отправлено в СФР, ответ не поступал'
                else:
                    answer = 'Не отправлено в СФР'
                import_id = rec.keeped_report_id
        else:
            answer = '---'
        # ['Фамилия, имя, отчество', 'Дата рождения', 'Личный номер', 'Субъект', 'Рег. номер импорта', 'Протокол СФР', 'Ответ СФР']
        return [
            '{} {} {}'.format(
                self.model.linked_person.picked_last_name.value,
                self.model.linked_person.picked_first_name.value,
                self.model.linked_person.picked_middle_name.value
            ),
            self.model.linked_person.birthday,
            self.model.picked_personal_number.value,
            self.model.picked_military_subject.value,
            import_id,
            prot_sfr,
            answer
        ]


class DefendersListData:

    def __init__(self, app):
        self.app = app

    @property
    def session(self):
        return self.app.database.session

    def get_data(self, filter_text):
        rows = []
        if filter_text:
            filter_parts = filter_text.split(' ')

            models = self.session.query(LinkedDefender)
            models = models.join(LinkedPerson)
            models = models.join(PickedLastName)
            models = models.join(PickedFirstName)
            models = models.join(PickedMiddleName)
            models = models.join(PickedPersonalNumber)

            for part in filter_parts:
                if part:
                    models = models.filter(
                        or_(
                            ilike_op(PickedLastName.value, '%{}%'.format(part)),
                            ilike_op(PickedFirstName.value, '%{}%'.format(part)),
                            ilike_op(PickedMiddleName.value, '%{}%'.format(part)),
                            ilike_op(PickedPersonalNumber.value, '%{}%'.format(part))
                        )
                    )

            models = models.order_by(
                PickedLastName.value,
                PickedFirstName.value,
                PickedMiddleName.value
            )
            models = models.all()

            zero_count = len(str(len(models)))
            for index, model in enumerate(models):
                defender = DefenderData(self.app)
                defender.model = model
                rows.append([str(index + 1).zfill(zero_count)] + defender.table_model_row())
        if not rows:
            rows.append(['---', 'Уточните критерии поиска'])
        return rows
