from backend import DefendersApp
from database import LinkedPerson, LinkedDefender, KeepedReportRecord

from tools import DTConvert


class Extruder:

    def __init__(self, session):
        self.session = session

        self.print_control_numbers()

        self.fucking_persons_ids = self.get_fucking_persons()
        print('Fucking persons <{}> found'.format(len(self.fucking_persons_ids)))

        self.fucking_defenders_ids = self.get_fucking_defenders()
        print('Fucking defenders <{}> found'.format(len(self.fucking_defenders_ids)))

        self.change_persons_ids()
        self.delete_fuckings()

        self.print_control_numbers()

        self.session.commit()
        q = 1

    def print_control_numbers(self):
        persons = self.session.query(LinkedPerson).all()
        persons = len(persons)

        defenders = self.session.query(LinkedDefender).all()
        defenders = len(defenders)

        records = self.session.query(KeepedReportRecord).all()
        records = len(records)

        print('CONTROL: persons - {}, defenders - {}, records - {}'.format(persons, defenders, records))

    def get_good_person(self, fucking_person: LinkedPerson, birthday: str) -> LinkedPerson:
        good_person = self.session.query(LinkedPerson).filter(
            LinkedPerson.eskk_gender_id == fucking_person.eskk_gender_id,
            LinkedPerson.picked_snils_id == fucking_person.picked_snils_id,
            LinkedPerson.picked_last_name_id == fucking_person.picked_last_name_id,
            LinkedPerson.picked_first_name_id == fucking_person.picked_first_name_id,
            LinkedPerson.picked_middle_name_id == fucking_person.picked_middle_name_id,
            LinkedPerson.birthday == birthday
        ).scalar()
        return good_person

    def get_fucking_persons(self) -> dict:
        result = {}  # ключ - fucking id, значение - good id
        fucking_persons = self.session.query(LinkedPerson).all()
        for fucking_person in fucking_persons:  # по-умолчанию каждая модель считается fucking
            birthday = DTConvert(fucking_person.birthday).dstring  # конвертация даты в принятый вид
            good_person = self.get_good_person(fucking_person, birthday)  # попытка найти модель good
            if good_person:  # good модель найдена
                if good_person.id != fucking_person.id:  # id не совпадает, fucking подтвердился
                    result[fucking_person.id] = good_person.id
                else:  # id совпадает, нашел сам себя
                    pass
            elif birthday:  # good модель не найдена, дата рождения не нулевая
                fucking_person.birthday = birthday  # меняем birthday на правильное написание
                self.session.flush()
            else:  # нулевая дата рождения или не смогла конвертироваться
                print('Birthday <{}> is strange?'.format(fucking_person.birthday))
        return result

    def get_good_defender(self, fucking_defender: LinkedDefender, good_person_id: str) -> LinkedDefender:
        good_defender = self.session.query(LinkedDefender).filter(
            LinkedDefender.linked_person_id == good_person_id,
            LinkedDefender.linked_document_id == fucking_defender.linked_document_id,
            LinkedDefender.linked_document_vbd_id == fucking_defender.linked_document_vbd_id,
            LinkedDefender.linked_reg_address_id == fucking_defender.linked_reg_address_id,
            LinkedDefender.linked_fact_address_id == fucking_defender.linked_fact_address_id,
            LinkedDefender.picked_military_subject_id == fucking_defender.picked_military_subject_id,
            LinkedDefender.picked_personal_number_id == fucking_defender.picked_personal_number_id,
            LinkedDefender.birth_place == fucking_defender.birth_place,
            LinkedDefender.exclude_date == fucking_defender.exclude_date,
            LinkedDefender.exclude_order == fucking_defender.exclude_order,
            LinkedDefender.id_ern == fucking_defender.id_ern
        ).scalar()
        return good_defender

    def get_fucking_defenders(self) -> dict:
        result = {}  # ключ - fucking id, значение - good id
        for fucking_person_id in self.fucking_persons_ids:
            good_person_id = self.fucking_persons_ids[fucking_person_id]
            fucking_defenders = self.session.query(LinkedDefender).filter(
                LinkedDefender.linked_person_id == fucking_person_id
            ).all()
            for fucking_defender in fucking_defenders:
                good_defender = self.get_good_defender(fucking_defender, good_person_id)
                if good_defender:  # good модель найдена
                    if good_defender.id != fucking_defender.id:  # id не совпадает, fucking подтвердился
                        result[fucking_defender.id] = good_defender.id
                    else:  # id совпадает, нашел сам себя
                        pass
                else:
                    # подменяем fucking person id на good person id
                    fucking_defender.linked_person_id = good_person_id
                    self.session.flush()
        return result

    def change_persons_ids(self):
        for fucking_person_id in self.fucking_persons_ids:
            good_person_id = self.fucking_persons_ids[fucking_person_id]
            linked_defenders = self.session.query(LinkedDefender).filter(
                LinkedDefender.linked_person_id == fucking_person_id
            ).all()
            for linked_defender in linked_defenders:
                if linked_defender.id in self.fucking_defenders_ids:
                    fucking_defender_id = linked_defender.id
                    good_defender_id = self.fucking_defenders_ids[linked_defender.id]
                    self.change_defender_id(fucking_defender_id, good_defender_id)
                else:
                    linked_defender.linked_person_id = good_person_id
                self.session.flush()

    def change_defender_id(self, fucking_defender_id: str, good_defender_id: str):
        keeped_records = self.session.query(KeepedReportRecord).filter(
            KeepedReportRecord.linked_defender_id == fucking_defender_id
        ).all()
        for keeped_record in keeped_records:
            keeped_record.linked_defender_id = good_defender_id
            self.session.flush()

    def delete_fuckings(self):
        count = 0

        persons_without_defender = self.session.query(LinkedPerson).filter(LinkedPerson.linked_defenders is None).all()

        for fucking_person_id in self.fucking_persons_ids:
            defenders = self.session.query(LinkedDefender).filter(
                LinkedDefender.linked_person_id == fucking_person_id
            ).all()
            count += len(defenders)
            for defender in defenders:
                if not defender.keeped_report_records:
                    self.session.delete(defender)
                    self.session.flush()
                else:
                    raise KeyError('KeepedRecord contains fucking LinkedDefender.id')
        print(
            'Deleted defenders with fucking persons ids ={}, persons without defender ={}'.format(
                count,
                len(persons_without_defender)
            )
        )

        defenders_without_record = self.session.query(LinkedDefender).filter(LinkedDefender.keeped_report_records is None).all()

        count = 0
        for fucking_defender_id in self.fucking_defenders_ids:
            records = self.session.query(KeepedReportRecord).filter(
                KeepedReportRecord.linked_defender_id == fucking_defender_id
            ).all()
            count += len(records)
        print(
            'Deleted records with fucking defenders ids ={}, defenders_without_record ={}'.format(
                count,
                len(defenders_without_record)
            )
        )

        count = 0
        for fucking_person_id in self.fucking_persons_ids:
            person = self.session.query(LinkedPerson).filter(
                LinkedPerson.id == fucking_person_id
            ).scalar()
            if person:
                count += 1
                self.session.delete(person)
                self.session.flush()
        print('Deleted persons with fucking persons ids ={}'.format(count))


if __name__ == "__main__":
    app = DefendersApp()
    extruder = Extruder(app.database.session)
