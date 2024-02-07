from sqlalchemy import or_
from sqlalchemy.sql.operators import ilike_op

from database import LinkedDefender, LinkedPerson, PickedLastName, PickedFirstName, PickedMiddleName, PickedPersonalNumber, LinkedOrderPerson, LinkedOrderFIO


class ParticipantData:

    def __init__(self, app):
        self.app = app
        self.model = None

    @property
    def session(self):
        return self.app.database.session

    def get_participant(self, defender_id):
        pass

    def table_model_row(self):
        return [
            self.model.picked_military_rank.value,
            self.model.linked_order_fio.person_appeal,
            self.model.picked_personal_number.value,
            self.model.picked_military_subject.value
        ]


class ParticipantsListData:

    def __init__(self, app):
        self.app = app

    @property
    def session(self):
        return self.app.database.session

    def get_data(self, filter_text):
        rows = []
        if filter_text:
            filter_parts = filter_text.split(' ')

            models = self.session.query(LinkedOrderPerson)
            models = models.join(LinkedOrderFIO)
            models = models.join(PickedLastName)
            models = models.join(PickedFirstName)
            models = models.join(PickedMiddleName)
            models = models.join(PickedPersonalNumber)

            for part in filter_parts:
                if part:
                    models = models.filter(
                        or_(
                            PickedLastName.value.ilike('%{}%'.format(part)),
                            PickedFirstName.value.ilike('%{}%'.format(part)),
                            PickedMiddleName.value.ilike('%{}%'.format(part)),
                            PickedPersonalNumber.value.ilike('%{}%'.format(part))
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
                participant = ParticipantData(self.app)
                participant.model = model
                rows.append([str(index + 1).zfill(zero_count)] + participant.table_model_row())
        # if not rows:
        #     rows.append(['---', 'Уточните критерии поиска'])
        return rows
